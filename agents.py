"""
Skillora AI - Multi-Agent Engine & Smart Adapt AI Architecture
Coordinates 5 Specialized Agents:
1. Skill Analyzer Agent (Auditing strengths, weaknesses, skill report)
2. Career Guide Agent (Industry benchmarking, career readiness formula, gap analysis)
3. Learning Planner Agent (Synthesizing 4-stage journey: Discover, Develop, Create, Achieve)
4. Progress Evaluator Agent (Assessment scoring, Smart Adapt AI logic, project evaluation)
5. AI Mentor Agent (Conversational counsel, daily goals, orchestrating agent sync)
"""

import json
import sqlite3
import datetime
import uuid
from database import get_db, CAREER_BENCHMARKS

# Assessment Quiz Bank
QUIZ_BANK = {
    "quiz_discover": {
        "title": "Stage 1: Discover – Foundations & Mental Models Diagnostic",
        "topic": "Frontend Fundamentals & Core Logic",
        "description": "Assess HTML5 semantic architecture, CSS Flexbox axis flow, and modern JavaScript variable semantics.",
        "questions": [
            {
                "id": "qd_1",
                "question": "Which CSS Flexbox property controls how flex items are aligned along the cross axis inside their container?",
                "options": [
                    "justify-content",
                    "align-items",
                    "flex-direction",
                    "align-content"
                ],
                "correct": 1,
                "explanation": "`align-items` aligns items along the cross axis (vertical in row direction), whereas `justify-content` aligns along the main axis.",
                "concept": "CSS Flexbox Cross Axis"
            },
            {
                "id": "qd_2",
                "question": "What is the primary architectural purpose of semantic HTML tags like `<main>`, `<article>`, and `<nav>`?",
                "options": [
                    "They trigger hardware GPU acceleration for animations.",
                    "They convey structural meaning to search engines and assistive screen readers (A11y).",
                    "They automatically bundle external CSS stylesheets.",
                    "They enforce strict typing on inner text elements."
                ],
                "correct": 1,
                "explanation": "Semantic HTML tags improve web accessibility (A11y) and SEO by declaring the meaningful purpose of content regions to assistive devices and web crawlers.",
                "concept": "Semantic HTML & Accessibility"
            },
            {
                "id": "qd_3",
                "question": "What evaluates in JavaScript when executing `console.log(typeof null)`?",
                "options": [
                    "'null'",
                    "'undefined'",
                    "'object'",
                    "'boolean'"
                ],
                "correct": 2,
                "explanation": "`typeof null` returns `'object'` in JavaScript due to a historical legacy artifact in the original JS engine type tag representation.",
                "concept": "JavaScript Type Coercion"
            },
            {
                "id": "qd_4",
                "question": "In modern ES6+, what distinguishes `const` from `let` declarations?",
                "options": [
                    "`let` is block-scoped, while `const` is function-scoped.",
                    "`let` allows reassigning variable bindings, while `const` creates an immutable binding to a memory reference.",
                    "`const` values can never contain nested mutable properties (e.g. in objects or arrays).",
                    "`const` is hoisted with its initial value, while `let` is not."
                ],
                "correct": 1,
                "explanation": "`let` permits reassignment within its block scope, whereas `const` prohibits reassigning the identifier binding (though object properties may still be modified).",
                "concept": "ES6 Lexical Scoping"
            },
            {
                "id": "qd_5",
                "question": "How does the browser event loop treat Promise callbacks (Microtasks) relative to `setTimeout` callbacks (Macrotasks)?",
                "options": [
                    "Microtasks have strict priority and are completely drained before the next macrotask is executed.",
                    "`setTimeout` always executes ahead of unresolved microtasks.",
                    "Both share an identical FIFO queue without execution priority.",
                    "Microtasks are handled in parallel background web workers."
                ],
                "correct": 0,
                "explanation": "Microtasks (Promises, queueMicrotask) have strict execution priority and are drained immediately when the call stack clears, before the browser picks the next Macrotask.",
                "concept": "Event Loop Microtasks"
            }
        ]
    },
    "quiz_develop": {
        "title": "Stage 2: Develop – React Architecture & Backend Execution",
        "topic": "React Hooks & Express Services",
        "description": "Assess state immutability, lifecycle hooks, and Express RESTful routing principles.",
        "questions": [
            {
                "id": "qdev_1",
                "question": "Why must state in React never be mutated directly (e.g. `state.count = 5`)?",
                "options": [
                    "Direct mutation throws an uncatchable syntax error.",
                    "React relies on shallow reference equality (`Object.is`) to detect state changes and trigger UI re-renders.",
                    "It causes memory leaks in the garbage collector.",
                    "Components cannot read mutated values."
                ],
                "correct": 1,
                "explanation": "React compares previous and next state references. In-place mutation preserves the exact memory address, meaning React skips scheduled UI re-renders.",
                "concept": "React State Immutability"
            },
            {
                "id": "qdev_2",
                "question": "What happens if you omit the dependency array in a React `useEffect(callback)` hook?",
                "options": [
                    "The effect executes only once upon mounting.",
                    "The effect executes after every single render cycle of that component.",
                    "The effect never executes.",
                    "React logs a runtime compilation warning."
                ],
                "correct": 1,
                "explanation": "Omitting the dependency array causes the effect to run after every render cycle. Passing `[]` runs it once on mount; passing `[dep]` runs it only when `dep` changes.",
                "concept": "React Hook Lifecycles"
            },
            {
                "id": "qdev_3",
                "question": "In Express.js middleware, what is the role of invoking `next()`?",
                "options": [
                    "It terminates the HTTP request and sends an empty 200 response.",
                    "It passes control to the subsequent middleware function in the request pipeline stack.",
                    "It restarts the server process.",
                    "It commits a database transaction."
                ],
                "correct": 1,
                "explanation": "Calling `next()` passes execution control to the next registered middleware or route handler in the Express request-response stack.",
                "concept": "Express Middleware Stack"
            },
            {
                "id": "qdev_4",
                "question": "Which HTTP status code is most appropriate when a client request lacks valid authentication credentials (e.g. missing or expired JWT token)?",
                "options": [
                    "400 Bad Request",
                    "401 Unauthorized",
                    "403 Forbidden",
                    "404 Not Found"
                ],
                "correct": 1,
                "explanation": "401 Unauthorized denotes that the requested resource requires valid user authentication credentials.",
                "concept": "RESTful Status Codes"
            }
        ]
    }
}

class MultiAgentEngine:
    """
    Coordinates Agent 1 through Agent 5 with structured exchange logs,
    Smart Adapt AI calibration, and automated project evaluation.
    """

    def __init__(self, db_conn=None):
        self.conn = db_conn or get_db()

    def log_agent_exchange(self, learner_id, agent_name, agent_role, target_agent, action, message, payload=None):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO agent_exchange_logs (
            learner_id, agent_name, agent_role, target_agent, action, message, payload
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            learner_id,
            agent_name,
            agent_role,
            target_agent,
            action,
            message,
            json.dumps(payload) if payload else None
        ))
        self.conn.commit()

    # Agent 1: Skill Analyzer Agent
    def run_skill_analyzer(self, learner_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM skills WHERE learner_id = ?", (learner_id,))
        skills = [dict(row) for row in cursor.fetchall()]

        mastered = [s for s in skills if s["state"] == "mastered"]
        learning = [s for s in skills if s["state"] == "learning"]
        missing = [s for s in skills if s["state"] == "missing"]
        recommended = [s for s in skills if s["state"] == "recommended"]

        strengths = [s["name"] for s in skills if s["proficiency"] >= 60]
        critical_gaps = [s["name"] for s in skills if s["state"] == "missing" and s["importance"] == "Critical"]

        report = {
            "total_tracked": len(skills),
            "mastered_count": len(mastered),
            "learning_count": len(learning),
            "missing_count": len(missing),
            "recommended_count": len(recommended),
            "strengths": strengths,
            "critical_gaps": critical_gaps,
            "summary": f"Identified {len(strengths)} confirmed strengths ({', '.join(strengths)}). Flagged {len(critical_gaps)} critical gaps requiring systematic bridges."
        }

        self.log_agent_exchange(
            learner_id,
            "Skill Analyzer Agent",
            "Skill Discovery",
            "Career Guide Agent",
            "SKILL_AUDIT_COMPLETE",
            f"Audit finished: {len(strengths)} verified strengths, {len(missing)} missing gaps isolated.",
            report
        )
        return report

    # Agent 2: Career Guide Agent
    def run_career_guide(self, learner_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM learners WHERE id = ?", (learner_id,))
        learner = dict(cursor.fetchone())

        career_goal = learner["career_goal"]
        benchmark = CAREER_BENCHMARKS.get(career_goal, CAREER_BENCHMARKS["Full Stack Developer"])

        cursor.execute("SELECT * FROM skills WHERE learner_id = ?", (learner_id,))
        skills_dict = {s["name"].lower(): dict(s) for s in cursor.fetchall()}

        # Calculate Career Readiness Score
        total_benchmark_points = 0
        earned_points = 0
        matching_skills = []
        missing_skills = []

        for req in benchmark["core_competencies"]:
            req_name = req["name"]
            req_lower = req_name.lower()
            target_level = req["target"]
            weight = 1.5 if req["importance"] == "Critical" else 1.0

            total_benchmark_points += target_level * weight

            matched = False
            s_words = [w for w in req_lower.replace("&", " ").replace("/", " ").replace("-", " ").split() if len(w) > 2]
            for s_name, s_data in skills_dict.items():
                my_words = [w for w in s_name.replace("&", " ").replace("/", " ").replace("-", " ").split() if len(w) > 2]
                is_match = (s_name in req_lower or req_lower in s_name or
                            any(mw in req_lower for mw in my_words) or
                            any(sw in s_name for sw in s_words))
                if is_match:
                    prof = s_data["proficiency"]
                    if s_data.get("state") != "missing" and prof >= 25:
                        earned_points += min(prof, target_level) * weight
                        matched = True
                        matching_skills.append({
                            "name": req_name,
                            "proficiency": prof,
                            "target": target_level,
                            "importance": req["importance"]
                        })
                    break

            if not matched:
                missing_skills.append({
                    "name": req_name,
                    "target": target_level,
                    "importance": req["importance"],
                    "category": req["category"]
                })

        # Roadmap progress component (20%)
        cursor.execute("""
        SELECT COUNT(*) as total_items,
               SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_items
        FROM roadmap_items i
        JOIN roadmap_stages s ON i.stage_id = s.id
        WHERE s.learner_id = ?
        """, (learner_id,))
        item_stats = dict(cursor.fetchone())
        roadmap_ratio = (item_stats["completed_items"] / max(item_stats["total_items"], 1)) if item_stats["total_items"] else 0

        # Skill-to-Project Bridge completed count (15%)
        cursor.execute("SELECT COUNT(*) as completed_count FROM skill_projects WHERE learner_id = ? AND status = 'completed'", (learner_id,))
        completed_projects = cursor.fetchone()["completed_count"]
        project_ratio = min(completed_projects / 4.0, 1.0)

        # Assessments passed bonus (up to 8%)
        cursor.execute("SELECT COUNT(*) as passed_count FROM assessments WHERE learner_id = ? AND percentage >= 60", (learner_id,))
        passed_assessments = cursor.fetchone()["passed_count"]
        assessment_bonus = min(passed_assessments * 4, 8)

        # Weighted Readiness Score:
        # Aptitude baseline: 20%
        # Skill Match: up to 40%
        # Roadmap Tasks: up to 20%
        # Projects: up to 15%
        # Assessment Bonus: up to 8%
        aptitude_baseline = 20.0
        skill_match_component = (earned_points / max(total_benchmark_points, 1)) * 40.0
        roadmap_component = roadmap_ratio * 20.0
        project_component = project_ratio * 15.0

        raw_readiness = aptitude_baseline + skill_match_component + roadmap_component + project_component + assessment_bonus
        final_readiness = int(min(max(round(raw_readiness), 20), 100))

        # Overall skill strength
        skill_strength = int(min(max(round((earned_points / max(total_benchmark_points, 1)) * 100 + 15), 20), 100))

        # Update learner table
        cursor.execute("""
        UPDATE learners
        SET readiness_score = ?, skill_strength = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (final_readiness, skill_strength, learner_id))
        self.conn.commit()

        analysis = {
            "career_goal": career_goal,
            "readiness_score": final_readiness,
            "skill_strength": skill_strength,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "market_demand": benchmark["market_demand"],
            "avg_salary_range": benchmark["avg_salary_range"],
            "summary": f"Target: {career_goal}. Career Readiness calculated at {final_readiness}%. {len(matching_skills)} matching proficiencies, {len(missing_skills)} critical gaps prioritized."
        }

        self.log_agent_exchange(
            learner_id,
            "Career Guide Agent",
            "Benchmark Analysis",
            "Learning Planner Agent",
            "READINESS_CALIBRATED",
            f"Readiness calculated at {final_readiness}% for {career_goal}. Identified {len(missing_skills)} gaps to bridge.",
            analysis
        )
        return analysis

    # Agent 3: Learning Planner Agent
    def run_learning_planner(self, learner_id, regenerate_roadmap=False):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM learners WHERE id = ?", (learner_id,))
        learner = dict(cursor.fetchone())

        career_goal = learner["career_goal"]

        if regenerate_roadmap:
            # Clear old roadmap items & stages for this learner
            cursor.execute("SELECT id FROM roadmap_stages WHERE learner_id = ?", (learner_id,))
            stage_ids = [r["id"] for r in cursor.fetchall()]
            for sid in stage_ids:
                cursor.execute("DELETE FROM roadmap_items WHERE stage_id = ?", (sid,))
            cursor.execute("DELETE FROM roadmap_stages WHERE learner_id = ?", (learner_id,))
            self.conn.commit()

            # Rebuild 4-Stage Learning Journey
            self._generate_custom_journey(learner_id, career_goal)

        cursor.execute("SELECT COUNT(*) as stage_count FROM roadmap_stages WHERE learner_id = ?", (learner_id,))
        count = cursor.fetchone()["stage_count"]

        self.log_agent_exchange(
            learner_id,
            "Learning Planner Agent",
            "Roadmap Synthesis",
            "Progress Evaluator Agent",
            "JOURNEY_STRUCTURED",
            f"4-Stage Journey dynamically constructed for '{career_goal}'. Discover -> Develop -> Create -> Achieve aligned.",
            {"stages_active": count, "career_goal": career_goal}
        )
        return {"status": "success", "stages_count": count}

    def _generate_custom_journey(self, learner_id, career_goal):
        cursor = self.conn.cursor()
        if career_goal == "Data Scientist & AI Specialist":
            stages = [
                ("da_s1", learner_id, "discover", 1, "Stage 1: Discover", "Foundations of High-Dimensional Data",
                 "Python data structures, NumPy vectorization, exploratory statistics, and linear algebra mental models.", 24, "active"),
                ("da_s2", learner_id, "develop", 2, "Stage 2: Develop", "Statistical Modeling & Scikit-Learn Algorithms",
                 "Regression, decision trees, feature engineering, and cross-validation pipelines.", 32, "pending"),
                ("da_s3", learner_id, "create", 3, "Stage 3: Create", "Predictive Analytics & Deep Learning PyTorch",
                 "Neural network architectures, PyTorch loss backprop, and interactive Tableau dashboards.", 38, "pending"),
                ("da_s4", learner_id, "achieve", 4, "Stage 4: Achieve", "Production MLOps & Generative AI Systems",
                 "RAG pipelines with ChromaDB, model containerization, latency profiling, and mock technical interview.", 22, "pending")
            ]
            items = [
                ("da_i1", "da_s1", "NumPy Matrix Operations & Vector Math", "Deconstruct broadcasting, dot products, and multi-dimensional arrays.", "concept", "3 hrs", 1, 0, 0, "NumPy Guide", "https://numpy.org"),
                ("da_i2", "da_s1", "Pandas DataFrames, GroupBy & Time Series", "Wrangle real-world financial and customer datasets cleanly.", "drill", "4 hrs", 0, 0, 0, "Pandas Docs", "https://pandas.pydata.org"),
                ("da_i3", "da_s1", "Stage 1 Foundations Diagnostic Quiz", "Adaptive evaluation on vector algebra and SQL aggregation logic.", "quiz", "30 mins", 0, 0, 0, "Stage 1 Quiz", "quiz_discover"),
                ("da_i4", "da_s2", "Feature Engineering, Scaling & Missing Data", "Outlier detection, one-hot encoding, and normalization strategies.", "drill", "5 hrs", 0, 0, 0, "Scikit-Learn Guide", "https://scikit-learn.org"),
                ("da_i5", "da_s3", "Interactive Churn Predictor & Revenue Risk Project", "Build end-to-end classification pipeline with model metrics.", "project", "8 hrs", 0, 0, 0, "Project Bridge", "project_data_pipeline")
            ]
        elif career_goal == "Cloud & DevOps Engineer":
            stages = [
                ("cd_s1", learner_id, "discover", 1, "Stage 1: Discover", "Linux Core, Shell Scripting & Networking",
                 "File permissions, process management, TCP/IP, DNS routing, and Git collaboration.", 22, "active"),
                ("cd_s2", learner_id, "develop", 2, "Stage 2: Develop", "Docker Containers & Microservice Isolation",
                 "Multi-stage Dockerfiles, image optimization, and multi-container Docker Compose.", 32, "pending"),
                ("cd_s3", learner_id, "create", 3, "Stage 3: Create", "Kubernetes Clusters & Automated CI/CD",
                 "Deploying pods, services, ingress controllers, and GitHub Actions continuous delivery.", 40, "pending"),
                ("cd_s4", learner_id, "achieve", 4, "Stage 4: Achieve", "Infrastructure as Code & SRE Observability",
                 "Terraform cloud provisioning, Prometheus monitoring, and disaster recovery drills.", 24, "pending")
            ]
            items = [
                ("cd_i1", "cd_s1", "Linux Administration & Bash Automation", "Systemd services, cron jobs, user groups, and log analysis.", "concept", "3.5 hrs", 1, 0, 0, "Linux Foundation", "https://linuxfoundation.org"),
                ("cd_i2", "cd_s1", "TCP/IP, Reverse Proxies & Nginx Configuration", "Configure reverse proxies, SSL certificates, and firewall rules.", "drill", "4 hrs", 0, 0, 0, "Nginx Docs", "https://nginx.org"),
                ("cd_i3", "cd_s2", "Docker Containerization & Layer Caching", "Write slim Alpine images with reproducible dependency locks.", "drill", "5 hrs", 0, 0, 0, "Docker Docs", "https://docs.docker.com"),
                ("cd_i4", "cd_s3", "GitHub Actions Production CI/CD Pipeline", "Automate build, lint, unit tests, and image registry pushes.", "project", "6 hrs", 0, 0, 0, "GitHub Actions", "https://actions.github.com")
            ]
        else: # Default: Full Stack Developer
            stages = [
                ("fs_s1", learner_id, "discover", 1, "Stage 1: Discover", "Uncover Foundations & Mental Models",
                 "Deconstruct web architecture, explore semantic HTML5 structure, and master modern CSS visual layout mechanics.", 24, "active"),
                ("fs_s2", learner_id, "develop", 2, "Stage 2: Develop", "Build Essential Technical Execution",
                 "Deep-dive into modern JavaScript ES6+, reactive component architecture with React, and asynchronous server runtimes with Node.js.", 36, "pending"),
                ("fs_s3", learner_id, "create", 3, "Stage 3: Create", "Complete Practical Real-World Projects",
                 "Architect and deliver working applications: Interactive Calculator, Developer Portfolio, REST API Service, and Relational Database.", 42, "pending"),
                ("fs_s4", learner_id, "achieve", 4, "Stage 4: Achieve", "Demonstrate Career Readiness & Impact",
                 "End-to-end cloud deployment, CI/CD pipelines, security hardening, performance profiling, and simulated hiring interviews.", 20, "pending")
            ]
            items = [
                ("fs_i1", "fs_s1", "Semantic HTML5 Architecture & Screen Reader A11y", "Structure modern web documents with header, nav, main, and WCAG accessibility standards.", "concept", "2.5 hrs", 1, 0, 0, "MDN Semantic Web", "https://developer.mozilla.org"),
                ("fs_i2", "fs_s1", "CSS Box Model & Fluid Typography Foundations", "Master margins, padding, border-box sizing, and fluid CSS variables.", "concept", "3 hrs", 1, 0, 0, "web.dev Box Model", "https://web.dev"),
                ("fs_i3", "fs_s1", "Interactive CSS Flexbox Mastery Drills", "Build responsive card grids, navigation bars, and alignment controls.", "drill", "3.5 hrs", 0, 0, 0, "Flexbox Froggy", "https://flexboxfroggy.com"),
                ("fs_i4", "fs_s1", "CSS Grid 2D Layouts & Responsive Breakpoints", "Design dashboard viewports without media query bloat.", "drill", "4 hrs", 0, 0, 0, "CSS Grid Garden", "https://cssgridgarden.com"),
                ("fs_i5", "fs_s1", "Foundational Diagnostics & Web Architecture Quiz", "Adaptive assessment evaluating semantic markup, layout rendering pipelines, and DOM structure.", "quiz", "30 mins", 0, 0, 0, "Stage 1 Diagnostic Quiz", "quiz_discover"),
                ("fs_i6", "fs_s2", "JavaScript ES6+ Syntax, Scoping & Closures", "Arrow functions, object destructuring, rest/spread operators, and lexical scoping.", "concept", "4.5 hrs", 0, 0, 0, "JavaScript.info", "https://javascript.info"),
                ("fs_i7", "fs_s2", "Asynchronous JavaScript: Promises & Event Loop", "Deconstruct microtasks vs macrotasks, async/await error propagation, and fetch.", "concept", "5 hrs", 0, 0, 0, "MDN Async JS", "https://developer.mozilla.org"),
                ("fs_i8", "fs_s2", "React Declarative Components, Props & Hooks", "Compose reusable component trees, manage state with useState, and effects with useEffect.", "drill", "6.5 hrs", 0, 0, 0, "React Docs", "https://react.dev"),
                ("fs_i9", "fs_s3", "Skill-to-Project Bridge: Interactive Calculator", "Build an interactive JavaScript stateful calculator component.", "project", "5 hrs", 0, 0, 0, "Project Bridge", "project_calculator"),
                ("fs_i10", "fs_s3", "Skill-to-Project Bridge: Developer Portfolio in React", "Craft an accessible, responsive personal portfolio with theme toggling.", "project", "8 hrs", 0, 0, 0, "Project Bridge", "project_portfolio"),
                ("fs_i11", "fs_s4", "Full Stack Simulated Technical Interview", "Comprehensive real-world scenario interview with coding challenge and system defense.", "quiz", "2 hrs", 0, 0, 0, "Final Career Simulation", "quiz_achieve")
            ]

        cursor.executemany("""
        INSERT INTO roadmap_stages (id, learner_id, stage_key, stage_number, title, tagline, description, duration_hours, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, stages)

        cursor.executemany("""
        INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, items)
        self.conn.commit()

    # Agent 4: Progress Evaluator Agent & Smart Adapt AI
    def evaluate_assessment(self, learner_id, quiz_id, answers):
        quiz = QUIZ_BANK.get(quiz_id)
        if not quiz:
            return {"error": "Quiz not found"}

        questions = quiz["questions"]
        correct_count = 0
        struggles = []
        details = []

        for i, q in enumerate(questions):
            user_choice = answers.get(q["id"])
            if user_choice is None:
                user_choice = answers.get(str(i))

            is_correct = (user_choice == q["correct"])
            if is_correct:
                correct_count += 1
            else:
                struggles.append(q["concept"])

            details.append({
                "id": q["id"],
                "question": q["question"],
                "user_choice": user_choice,
                "correct_choice": q["correct"],
                "is_correct": is_correct,
                "explanation": q["explanation"],
                "concept": q["concept"]
            })

        total = len(questions)
        pct = int(round((correct_count / max(total, 1)) * 100))
        cursor = self.conn.cursor()

        smart_adapt_action = "CONTINUE_TRAJECTORY"
        smart_adapt_message = ""

        # Smart Adapt AI Decision Engine:
        if pct < 50:
            # Score < 50%: AI recommends revision & beginner-friendly micro-drills
            smart_adapt_action = "SMART_ADAPT_REMEDIAL"
            smart_adapt_message = f"Smart Adapt AI Triggered: Diagnostic score ({pct}%) isolated conceptual friction in: {', '.join(set(struggles))}. Adding targeted foundation micro-drills to your roadmap."

            # Inject remedial item into current active stage
            cursor.execute("SELECT id FROM roadmap_stages WHERE learner_id = ? AND status = 'active' LIMIT 1", (learner_id,))
            active_stage = cursor.fetchone()
            stage_id = active_stage["id"] if active_stage else "stage_discover"

            remedial_item_id = f"remedial_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
            INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
            VALUES (?, ?, ?, ?, 'remedial', '1.5 hrs', 0, 1, 0, 'Targeted Foundation Drills', 'https://developer.mozilla.org')
            """, (
                remedial_item_id,
                stage_id,
                f"🧠 Smart Adapt Drill: Reinforcing {', '.join(set(struggles)) or 'Core Fundamentals'}",
                "Curated flashcards and 3 simplified interactive micro-exercises to reinforce memory models and core syntax without penalty."
            ))

            cursor.execute("""
            UPDATE learners
            SET smart_adapt_active = 1, smart_adapt_reason = ?
            WHERE id = ?
            """, (smart_adapt_message, learner_id))

            self.log_agent_exchange(
                learner_id,
                "Progress Evaluator Agent",
                "Performance Evaluation",
                "AI Mentor Agent",
                "SMART_ADAPT_REMEDIAL_TRIGGERED",
                f"Score {pct}% < 50%. Injected remedial micro-drill into active stage. Struggle topics: {', '.join(set(struggles))}.",
                {"score": pct, "struggles": struggles}
            )

            self.log_agent_exchange(
                learner_id,
                "AI Mentor Agent",
                "Personalized Guidance",
                "Deeksha (Learner)",
                "COMFORT_AND_PIVOT",
                f"Don't worry Deeksha! Learning is an evolutionary curve. I have adjusted your journey with simplified exercises on {', '.join(set(struggles))}. You'll build confidence step by step!",
                {"action": "encourage"}
            )

        elif pct >= 85:
            # Score >= 85%: Fast-track unlocked!
            smart_adapt_action = "SMART_ADAPT_FAST_TRACK"
            smart_adapt_message = f"Fast-Track AI Unlocked: Outstanding mastery ({pct}%)! Unlocked advanced elective topics and awarded the 'Diagnostic Vanguard' milestone."

            # Unlock achievement milestone
            cursor.execute("""
            UPDATE milestones
            SET achieved = 1, achieved_at = CURRENT_TIMESTAMP
            WHERE learner_id = ? AND category = 'Assessment'
            """, (learner_id,))

            # Inject advanced elective item
            cursor.execute("SELECT id FROM roadmap_stages WHERE learner_id = ? AND status = 'active' LIMIT 1", (learner_id,))
            active_stage = cursor.fetchone()
            stage_id = active_stage["id"] if active_stage else "stage_discover"

            fast_track_id = f"fasttrack_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
            INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
            VALUES (?, ?, ?, ?, 'advanced', '2 hrs', 0, 0, 1, 'Advanced Architecture Elective', 'https://web.dev')
            """, (
                fast_track_id,
                stage_id,
                "⚡ Fast-Track Elective: High-Performance CSS Layouts & Web Component Isolation",
                "Accelerated deep-dive designed for top performers: Explore CSS containment, subgrid, and modern web component paradigms."
            ))

            cursor.execute("""
            UPDATE learners
            SET smart_adapt_active = 1, smart_adapt_reason = ?
            WHERE id = ?
            """, (smart_adapt_message, learner_id))

            self.log_agent_exchange(
                learner_id,
                "Progress Evaluator Agent",
                "Performance Evaluation",
                "AI Mentor Agent",
                "SMART_ADAPT_FAST_TRACK_TRIGGERED",
                f"Score {pct}% >= 85%. Fast-track elective module unlocked and milestone awarded.",
                {"score": pct}
            )

            self.log_agent_exchange(
                learner_id,
                "AI Mentor Agent",
                "Personalized Guidance",
                "Deeksha (Learner)",
                "CELEBRATE_MASTERY",
                f"Incredible achievement Deeksha! Scoring {pct}% demonstrates exceptional comprehension of web architecture. Your Fast-Track bonus elective is now open!",
                {"action": "celebrate"}
            )
        else:
            smart_adapt_message = f"Solid progress! You scored {pct}%. Your learning roadmap continues on schedule."
            self.log_agent_exchange(
                learner_id,
                "Progress Evaluator Agent",
                "Performance Evaluation",
                "AI Mentor Agent",
                "ASSESSMENT_SCORED",
                f"Assessment scored at {pct}%. Target competency verified.",
                {"score": pct}
            )

        # Record assessment in database
        assessment_id = f"ass_{uuid.uuid4().hex[:8]}"
        cursor.execute("""
        INSERT INTO assessments (id, learner_id, quiz_id, quiz_title, score, max_score, percentage, smart_adapt_action, struggles_identified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            learner_id,
            quiz_id,
            quiz["title"],
            correct_count,
            total,
            pct,
            smart_adapt_action,
            json.dumps(struggles)
        ))

        self.conn.commit()
        # Recalculate Career Readiness
        self.run_career_guide(learner_id)

        return {
            "assessment_id": assessment_id,
            "quiz_title": quiz["title"],
            "score": correct_count,
            "max_score": total,
            "percentage": pct,
            "passed": pct >= 60,
            "struggles": struggles,
            "smart_adapt_action": smart_adapt_action,
            "smart_adapt_message": smart_adapt_message,
            "details": details
        }

    # Evaluate Skill-to-Project Bridge Submission
    def evaluate_project(self, learner_id, project_id, user_code):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM skill_projects WHERE id = ? AND learner_id = ?", (project_id, learner_id))
        proj = cursor.fetchone()
        if not proj:
            return {"error": "Project not found"}
        proj = dict(proj)

        keywords = json.loads(proj.get("solution_keywords") or "[]")
        matched = [k for k in keywords if k.lower() in user_code.lower()]
        score = int(round((len(matched) / max(len(keywords), 1)) * 100))
        passed = score >= 60

        feedback = []
        if passed:
            feedback.append(f"✅ Success! Your implementation cleanly satisfies core architectural constraints for '{proj['title']}'.")
            feedback.append(f"Validated key requirements: {', '.join(matched)}.")
        else:
            feedback.append("⚠️ Partial implementation detected. Make sure to implement proper state management, error handling, and syntax requirements.")
            missing = [k for k in keywords if k.lower() not in user_code.lower()]
            if missing:
                feedback.append(f"Consider integrating: {', '.join(missing)}.")

        feedback_str = " ".join(feedback)
        now_str = datetime.datetime.now().isoformat()

        cursor.execute("""
        UPDATE skill_projects
        SET status = ?, score = ?, feedback = ?, completed_at = ?
        WHERE id = ? AND learner_id = ?
        """, ("completed" if passed else "in_progress", score, feedback_str, now_str if passed else None, project_id, learner_id))

        # If passed, upgrade the associated skill in the Skill Universe!
        if passed:
            assoc_skill = proj["associated_skill"].split("&")[0].strip()
            cursor.execute("""
            UPDATE skills
            SET proficiency = MAX(proficiency, ?), state = 'mastered', notes = 'Verified through Skill-to-Project Bridge completion.'
            WHERE learner_id = ? AND name LIKE ?
            """, (score, learner_id, f"%{assoc_skill}%"))

            # Award Milestone
            cursor.execute("""
            UPDATE milestones
            SET achieved = 1, achieved_at = CURRENT_TIMESTAMP
            WHERE learner_id = ? AND category = 'Projects'
            """, (learner_id,))

        self.log_agent_exchange(
            learner_id,
            "Progress Evaluator Agent",
            "Project Evaluation",
            "AI Mentor Agent",
            "PROJECT_EVALUATED",
            f"Project '{proj['title']}' evaluated: Score {score}/100 ({'PASSED' if passed else 'IN_PROGRESS'}).",
            {"project_id": project_id, "score": score, "passed": passed}
        )

        self.log_agent_exchange(
            learner_id,
            "AI Mentor Agent",
            "Personalized Guidance",
            "Deeksha (Learner)",
            "PROJECT_FEEDBACK",
            f"Great job building in the Skill-to-Project Bridge! Creating practical working artifacts is what truly transforms missing skills into permanent strengths.",
            {"project_id": project_id, "score": score}
        )

        self.conn.commit()
        # Recalculate Career Readiness
        self.run_career_guide(learner_id)

        return {
            "project_id": project_id,
            "title": proj["title"],
            "score": score,
            "passed": passed,
            "feedback": feedback_str,
            "matched_requirements": matched
        }

    # Agent 5: AI Mentor Agent Contextual Chat
    def chat_with_mentor(self, learner_id, message, selected_agent=None):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM learners WHERE id = ?", (learner_id,))
        learner = dict(cursor.fetchone())

        career_goal = learner["career_goal"]
        readiness = learner["readiness_score"]
        msg_lower = message.lower()

        responder_agent = selected_agent or "AI Mentor Agent"
        reply = ""
        action_suggested = None

        if "career dna" in msg_lower or "potential" in msg_lower or "strength" in msg_lower:
            responder_agent = "Skill Analyzer Agent"
            reply = f"Hello {learner['name']}! Your Career DNA reveals high analytical depth (82) and debugging resilience (85). Your natural strength in structured relational thinking (SQL) and Python automation makes you an ideal candidate for full-stack data-intensive applications."
            action_suggested = "view_career_dna"

        elif "universe" in msg_lower or "skills" in msg_lower or "map" in msg_lower:
            responder_agent = "Skill Analyzer Agent"
            reply = f"In your Skill Universe, Python and SQL shine as mastered celestial nodes. Basic HTML is currently in progress. Your immediate growth priorities are CSS and JavaScript, which serve as foundational gateways to React and Node.js."
            action_suggested = "view_skill_universe"

        elif "readiness" in msg_lower or "score" in msg_lower or "matching" in msg_lower or "gap" in msg_lower:
            responder_agent = "Career Guide Agent"
            reply = f"Your current Career Readiness for {career_goal} is {readiness}%. We benchmark you across 10 industry hiring competencies. You have matched 3 core proficiencies, while 5 critical gaps (CSS, JavaScript, React, Node.js, API Integration) are actively bridged through your 4-stage journey."
            action_suggested = "view_career_explorer"

        elif "roadmap" in msg_lower or "journey" in msg_lower or "stage" in msg_lower or "next" in msg_lower:
            responder_agent = "Learning Planner Agent"
            reply = f"Your 4-Stage Learning Journey is structured across: Discover (Foundations), Develop (Execution), Create (Real Projects), and Achieve (Career Ready). Today's highest-leverage task is mastering CSS Flexbox & ES6 arrow functions in Stage 1."
            action_suggested = "view_learning_journey"

        elif "project" in msg_lower or "bridge" in msg_lower or "calculator" in msg_lower or "portfolio" in msg_lower:
            responder_agent = "Progress Evaluator Agent"
            reply = f"The Skill-to-Project Bridge is where knowledge transforms into demonstrable evidence! We have 4 practical mini-projects tailored to your missing skills: Interactive Calculator (JS), Developer Portfolio (React), REST API Service (Node.js), and Relational Schema (SQL)."
            action_suggested = "view_projects"

        elif "smart adapt" in msg_lower or "adapt" in msg_lower or "fail" in msg_lower or "quiz" in msg_lower:
            responder_agent = "Progress Evaluator Agent"
            reply = f"Smart Adapt AI is continuously watching over your learning velocity! If you score below 50% on any assessment, it automatically injects remedial micro-drills to strengthen weak concepts without penalizing your streak. If you score over 85%, it unlocks fast-track bonus electives!"
            action_suggested = "take_assessment"

        elif "future" in msg_lower or "future me" in msg_lower or "transform" in msg_lower:
            responder_agent = "AI Mentor Agent"
            reply = f"The 'Future Me' preview lets you visualize the exact professional you are becoming. By closing your current 5 skill gaps and completing your 4 bridge projects, your readiness score will climb from {readiness}% to 94%+!"
            action_suggested = "view_future_me"

        elif "change" in msg_lower and "goal" in msg_lower:
            responder_agent = "Career Guide Agent"
            reply = f"You can explore or switch your dream career anytime in the Career Explorer! When you do, all 5 of us collaborate instantly to recalibrate your Career DNA alignment and generate a brand-new 4-stage roadmap."
            action_suggested = "change_career_goal"

        else:
            responder_agent = "AI Mentor Agent"
            reply = f"Hey {learner['name']}! I'm your AI Mentor. Every skill has a purpose, and every learner has a future. Your daily goal today is: '{learner['daily_goal']}'. Let's invest 20 focused minutes to build your future today!"
            action_suggested = "daily_goal"

        self.log_agent_exchange(
            learner_id,
            responder_agent,
            "Personalized Guidance",
            "Deeksha (Learner)",
            "MENTOR_INTERACTION",
            f"User asked: '{message[:50]}...'. Replied: '{reply[:60]}...'",
            {"query": message, "responder": responder_agent}
        )

        return {
            "responder": responder_agent,
            "message": reply,
            "action_suggested": action_suggested,
            "timestamp": datetime.datetime.now().strftime("%I:%M %p")
        }

    # 5-Agent Collaborative Huddle
    def trigger_agent_collaboration(self, learner_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM learners WHERE id = ?", (learner_id,))
        learner = dict(cursor.fetchone())

        # Step 1: Skill Analyzer
        report = self.run_skill_analyzer(learner_id)
        # Step 2: Career Guide
        guide = self.run_career_guide(learner_id)
        # Step 3: Learning Planner
        planner = self.run_learning_planner(learner_id)

        huddle_flow = [
            {
                "agent": "Skill Analyzer Agent",
                "role": "Skill Discovery & Weakness Audit",
                "status": "Synchronized",
                "output": f"Audited {report['total_tracked']} skills. Confirmed {len(report['strengths'])} foundational strengths ({', '.join(report['strengths'])}). Flagged {len(report['critical_gaps'])} critical gaps: {', '.join(report['critical_gaps'])}."
            },
            {
                "agent": "Career Guide Agent",
                "role": "Industry Benchmark & Readiness Scoring",
                "status": "Synchronized",
                "output": f"Target: '{learner['career_goal']}'. Benchmarked across 10 industry criteria. Career Readiness calibrated at {guide['readiness_score']}%. Formulated prioritized bridges for missing competencies."
            },
            {
                "agent": "Learning Planner Agent",
                "role": "4-Stage Journey Synthesis",
                "status": "Synchronized",
                "output": "4-Stage Journey validated: Discover (24h) -> Develop (36h) -> Create (42h) -> Achieve (20h). Arranged beginner to advanced with 4 Skill-to-Project Bridge applications."
            },
            {
                "agent": "Progress Evaluator Agent",
                "role": "Smart Adapt AI Engine",
                "status": "Synchronized",
                "output": "Smart Adapt AI armed: Continuous monitoring active (<50% remedial revision, >85% fast-track privilege, repeated mistake isolation)."
            },
            {
                "agent": "AI Mentor Agent",
                "role": "Personalized Coaching & Daily Mission",
                "status": "Synchronized",
                "output": f"Synchronized daily learning mission for Deeksha: '{learner['daily_goal']}'. Motivation and progress forecasting ready."
            }
        ]

        return {
            "success": True,
            "learner_id": learner_id,
            "career_goal": learner["career_goal"],
            "readiness_score": guide["readiness_score"],
            "huddle_flow": huddle_flow
        }
