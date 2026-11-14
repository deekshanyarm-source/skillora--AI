"""
Skillora AI - Full-Stack Application Server
Serves static frontend assets and RESTful API endpoints for:
- Personalized Learner Profile
- Career DNA Diagnostics
- My Skill Universe Graph
- Career Explorer & Intelligent Matching
- 4-Stage Learning Journey (Discover, Develop, Create, Achieve)
- Skill-to-Project Bridge (Hands-on Mini Projects with Automated Scoring)
- Smart Adapt AI & Diagnostic Assessments
- Future Me Transformation Projection
- Multi-Agent Collaboration Huddle & AI Mentor
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from database import get_db, init_db, CAREER_BENCHMARKS
from agents import MultiAgentEngine, QUIZ_BANK

DEFAULT_PORT = 8081
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

class SkilloraHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status_code=200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        learner_id = query.get("learner_id", ["deeksha"])[0]

        if path.startswith("/api/"):
            self.handle_api_get(path, learner_id, query)
        else:
            if path in ("", "/"):
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        learner_id = payload.get("learner_id", "deeksha")

        if path.startswith("/api/"):
            self.handle_api_post(path, learner_id, payload)
        else:
            self._send_json({"error": "Endpoint not found"}, status_code=404)

    def handle_api_get(self, path, learner_id, query):
        conn = get_db()
        cursor = conn.cursor()
        engine = MultiAgentEngine(conn)

        if path == "/api/profile":
            cursor.execute("SELECT * FROM learners WHERE id = ?", (learner_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return self._send_json({"error": "Learner not found"}, status_code=404)
            learner = dict(row)

            # Get skill stats
            cursor.execute("""
            SELECT 
                COUNT(*) as total_skills,
                SUM(CASE WHEN state = 'mastered' THEN 1 ELSE 0 END) as mastered_count,
                SUM(CASE WHEN state = 'learning' THEN 1 ELSE 0 END) as learning_count,
                SUM(CASE WHEN state = 'missing' THEN 1 ELSE 0 END) as missing_count,
                SUM(CASE WHEN state = 'recommended' THEN 1 ELSE 0 END) as recommended_count
            FROM skills WHERE learner_id = ?
            """, (learner_id,))
            skills_stats = dict(cursor.fetchone())

            # Get milestone stats
            cursor.execute("""
            SELECT COUNT(*) as total_milestones,
                   SUM(CASE WHEN achieved = 1 THEN 1 ELSE 0 END) as achieved_count
            FROM milestones WHERE learner_id = ?
            """, (learner_id,))
            milestone_stats = dict(cursor.fetchone())

            conn.close()
            return self._send_json({
                "profile": learner,
                "skills_summary": skills_stats,
                "milestones_summary": milestone_stats
            })

        elif path == "/api/career-dna":
            cursor.execute("SELECT * FROM career_dna WHERE learner_id = ?", (learner_id,))
            dna_row = cursor.fetchone()
            if not dna_row:
                conn.close()
                return self._send_json({"error": "Career DNA not found"}, status_code=404)
            dna = dict(dna_row)
            dna["natural_strengths"] = json.loads(dna["natural_strengths"] or "[]")
            dna["growth_edges"] = json.loads(dna["growth_edges"] or "[]")
            dna["recommended_paths"] = json.loads(dna["recommended_paths"] or "[]")

            cursor.execute("SELECT readiness_score, skill_strength, career_goal FROM learners WHERE id = ?", (learner_id,))
            learner_info = dict(cursor.fetchone())

            conn.close()
            return self._send_json({
                "career_dna": dna,
                "readiness_score": learner_info["readiness_score"],
                "skill_strength": learner_info["skill_strength"],
                "career_goal": learner_info["career_goal"]
            })

        elif path == "/api/skill-universe":
            cursor.execute("SELECT * FROM skills WHERE learner_id = ? ORDER BY id ASC", (learner_id,))
            skills = []
            for r in cursor.fetchall():
                item = dict(r)
                item["prerequisites"] = json.loads(item["prerequisites"] or "[]")
                item["resources"] = json.loads(item["resources"] or "[]")
                item["connections"] = json.loads(item["connections"] or "[]")
                skills.append(item)

            conn.close()
            return self._send_json({"skills": skills})

        elif path == "/api/career-explorer":
            cursor.execute("SELECT career_goal, readiness_score, skill_strength FROM learners WHERE id = ?", (learner_id,))
            learner = dict(cursor.fetchone())
            analysis = engine.run_career_guide(learner_id)

            conn.close()
            return self._send_json({
                "current_career": learner["career_goal"],
                "all_careers": list(CAREER_BENCHMARKS.keys()),
                "career_details": CAREER_BENCHMARKS.get(learner["career_goal"], CAREER_BENCHMARKS["Full Stack Developer"]),
                "analysis": analysis
            })

        elif path == "/api/learning-journey":
            cursor.execute("SELECT * FROM roadmap_stages WHERE learner_id = ? ORDER BY stage_number ASC", (learner_id,))
            stages = [dict(s) for s in cursor.fetchall()]

            for s in stages:
                cursor.execute("""
                SELECT * FROM roadmap_items 
                WHERE stage_id = ? 
                ORDER BY id ASC
                """, (s["id"],))
                s["items"] = [dict(i) for i in cursor.fetchall()]

            conn.close()
            return self._send_json({"stages": stages})

        elif path == "/api/projects":
            cursor.execute("SELECT * FROM skill_projects WHERE learner_id = ? ORDER BY id ASC", (learner_id,))
            projects = []
            for r in cursor.fetchall():
                p = dict(r)
                p["objectives"] = json.loads(p["objectives"] or "[]")
                p["solution_keywords"] = json.loads(p["solution_keywords"] or "[]")
                projects.append(p)

            conn.close()
            return self._send_json({"projects": projects})

        elif path.startswith("/api/assessments/"):
            quiz_id = path.split("/")[-1]
            quiz = QUIZ_BANK.get(quiz_id)
            conn.close()
            if not quiz:
                return self._send_json({"error": "Assessment not found"}, status_code=404)
            # Send safe questions without correct answer index
            safe_quiz = {
                "id": quiz_id,
                "title": quiz["title"],
                "topic": quiz["topic"],
                "description": quiz["description"],
                "questions": [
                    {
                        "id": q["id"],
                        "question": q["question"],
                        "options": q["options"],
                        "concept": q["concept"]
                    } for q in quiz["questions"]
                ]
            }
            return self._send_json({"quiz": safe_quiz})

        elif path == "/api/future-me":
            cursor.execute("SELECT * FROM learners WHERE id = ?", (learner_id,))
            learner = dict(cursor.fetchone())

            cursor.execute("SELECT * FROM skills WHERE learner_id = ?", (learner_id,))
            all_skills = [dict(r) for r in cursor.fetchall()]
            mastered_now = [s["name"] for s in all_skills if s["state"] == "mastered"]
            missing_now = [s["name"] for s in all_skills if s["state"] == "missing"]

            cursor.execute("SELECT COUNT(*) as completed_count FROM skill_projects WHERE learner_id = ? AND status = 'completed'", (learner_id,))
            completed_projects = cursor.fetchone()["completed_count"]

            future_me = {
                "current_self": {
                    "title": "My Current Self",
                    "readiness_score": learner["readiness_score"],
                    "skill_strength": learner["skill_strength"],
                    "strengths": mastered_now,
                    "active_gaps": missing_now,
                    "projects_completed": completed_projects,
                    "stage": "Discover / Early Develop"
                },
                "future_self": {
                    "title": f"My Future Self ({learner['career_goal']})",
                    "projected_readiness_score": 96,
                    "projected_skill_strength": 92,
                    "mastered_competencies": mastered_now + missing_now,
                    "key_achievements": [
                        "Engineered 4 production-grade projects in Skill-to-Project Bridge",
                        "Achieved 90%+ in Full Stack Technical Interview Simulation",
                        "Mastered end-to-end Reactive UI with React & Scalable Express APIs",
                        "Automated CI/CD deployment pipeline with Docker & GitHub Actions"
                    ],
                    "target_market_readiness": "Senior Entry / Mid-Level Industry Hireable"
                }
            }
            conn.close()
            return self._send_json({"future_me": future_me})

        elif path == "/api/progress":
            cursor.execute("SELECT * FROM milestones WHERE learner_id = ? ORDER BY id ASC", (learner_id,))
            milestones = [dict(m) for m in cursor.fetchall()]

            cursor.execute("""
            SELECT * FROM agent_exchange_logs 
            WHERE learner_id = ? 
            ORDER BY id DESC LIMIT 15
            """, (learner_id,))
            logs = [dict(l) for l in cursor.fetchall()]

            cursor.execute("SELECT weekly_hours, learning_streak FROM learners WHERE id = ?", (learner_id,))
            learner = dict(cursor.fetchone())

            conn.close()
            return self._send_json({
                "milestones": milestones,
                "recent_logs": logs,
                "weekly_hours": learner["weekly_hours"],
                "learning_streak": learner["learning_streak"]
            })

        conn.close()
        return self._send_json({"error": "Endpoint not found"}, status_code=404)

    def handle_api_post(self, path, learner_id, payload):
        conn = get_db()
        cursor = conn.cursor()
        engine = MultiAgentEngine(conn)

        if path == "/api/career-explorer/switch":
            new_goal = payload.get("career_goal")
            if not new_goal or new_goal not in CAREER_BENCHMARKS:
                conn.close()
                return self._send_json({"error": "Invalid career goal"}, status_code=400)

            cursor.execute("UPDATE learners SET career_goal = ? WHERE id = ?", (new_goal, learner_id))
            conn.commit()

            # When dream career changes, ALL 5 agents re-evaluate and regenerate roadmap!
            engine.run_skill_analyzer(learner_id)
            engine.run_learning_planner(learner_id, regenerate_roadmap=True)
            guide = engine.run_career_guide(learner_id)

            engine.log_agent_exchange(
                learner_id,
                "Career Guide Agent",
                "Career Pivot",
                "All Agents",
                "CAREER_GOAL_SWITCHED",
                f"Dream career changed to '{new_goal}'. All 5 agents re-calibrated readiness ({guide['readiness_score']}%) and generated new 4-stage roadmap.",
                {"new_goal": new_goal, "readiness": guide["readiness_score"]}
            )

            conn.close()
            return self._send_json({
                "status": "success",
                "message": f"Career goal switched to {new_goal}. 5 Agents recalibrated roadmap.",
                "analysis": guide
            })

        elif path == "/api/learning-journey/toggle":
            item_id = payload.get("item_id")
            cursor.execute("SELECT completed FROM roadmap_items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if not item:
                conn.close()
                return self._send_json({"error": "Item not found"}, status_code=404)

            new_status = 0 if item["completed"] == 1 else 1
            cursor.execute("UPDATE roadmap_items SET completed = ? WHERE id = ?", (new_status, item_id))
            conn.commit()

            # Recalculate Career Readiness Score
            guide = engine.run_career_guide(learner_id)
            conn.close()
            return self._send_json({
                "status": "success",
                "item_id": item_id,
                "completed": new_status,
                "readiness_score": guide["readiness_score"]
            })

        elif path == "/api/projects/submit":
            project_id = payload.get("project_id")
            user_code = payload.get("code", "")
            result = engine.evaluate_project(learner_id, project_id, user_code)
            conn.close()
            return self._send_json(result)

        elif path == "/api/assessments/submit":
            quiz_id = payload.get("quiz_id")
            answers = payload.get("answers", {})
            result = engine.evaluate_assessment(learner_id, quiz_id, answers)
            conn.close()
            return self._send_json(result)

        elif path == "/api/mentor/chat":
            message = payload.get("message", "")
            selected_agent = payload.get("selected_agent")
            result = engine.chat_with_mentor(learner_id, message, selected_agent)
            conn.close()
            return self._send_json(result)

        elif path == "/api/agents/collaborate":
            result = engine.trigger_agent_collaboration(learner_id)
            conn.close()
            return self._send_json(result)

        elif path == "/api/profile/goal/toggle":
            cursor.execute("SELECT daily_goal_completed FROM learners WHERE id = ?", (learner_id,))
            current = cursor.fetchone()["daily_goal_completed"]
            new_val = 0 if current == 1 else 1
            cursor.execute("UPDATE learners SET daily_goal_completed = ? WHERE id = ?", (new_val, learner_id))
            conn.commit()
            conn.close()
            return self._send_json({"status": "success", "daily_goal_completed": new_val})

        elif path == "/api/skill-universe/toggle":
            skill_name = payload.get("name")
            state = payload.get("state", "learning")
            proficiency = int(payload.get("proficiency", 50))
            category = payload.get("category", "General")

            cursor.execute("SELECT id FROM skills WHERE learner_id = ? AND name = ?", (learner_id, skill_name))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("""
                UPDATE skills 
                SET state = ?, proficiency = ?, notes = 'Updated by learner'
                WHERE id = ?
                """, (state, proficiency, existing["id"]))
            else:
                cursor.execute("""
                INSERT INTO skills (learner_id, name, category, proficiency, state, importance, universe_x, universe_y, connections, notes)
                VALUES (?, ?, ?, ?, ?, 'Medium', 50, 50, '[]', 'Added by learner')
                """, (learner_id, skill_name, category, proficiency, state))

            conn.commit()
            guide = engine.run_career_guide(learner_id)
            conn.close()
            return self._send_json({"status": "success", "readiness_score": guide["readiness_score"]})

        elif path == "/api/demo/reset":
            init_db(force_reseed=True)
            conn.close()
            return self._send_json({"status": "success", "message": "Skillora AI reset to baseline Deeksha state."})

        conn.close()
        return self._send_json({"error": "Endpoint not found"}, status_code=404)

def run_server(port=None):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True

    # Render.com injects PORT env variable -- always honour it
    render_port = int(os.environ.get("PORT", 0)) or None
    resolved = port or render_port
    ports_to_try = [resolved] if resolved else [DEFAULT_PORT, 8082, 8000, 3000, 8083]
    for p in ports_to_try:
        if not p: continue
        try:
            httpd = socketserver.TCPServer(("", p), SkilloraHandler)
            print(f"Skillora AI server running at http://0.0.0.0:{p}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Shutting down server.")
            return
        except OSError as e:
            print(f"Port {p} unavailable: {e}. Trying next port...")

if __name__ == "__main__":
    import sys
    custom_port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_server(custom_port)
