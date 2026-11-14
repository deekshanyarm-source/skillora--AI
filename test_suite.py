"""
Skillora AI - Comprehensive Test Suite
Validates:
1. Initial profile seeding (Deeksha, Full Stack Developer, baseline readiness)
2. Skill Analyzer Agent discovery & gap isolation
3. Career Guide Agent benchmark & career readiness formula
4. Learning Planner Agent 4-Stage Journey (Discover, Develop, Create, Achieve)
5. Smart Adapt AI (<50% remedial drill injection, >85% fast-track privilege)
6. Skill-to-Project Bridge automated code evaluation & skill proficiency upgrade
7. AI Mentor Agent contextual dialogue & multi-agent routing
8. 5-Agent Collaborative Huddle synchronization
"""

import unittest
import json
from database import init_db, get_db
from agents import MultiAgentEngine, QUIZ_BANK

class TestSkilloraAI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db(force_reseed=True)

    def setUp(self):
        self.conn = get_db()
        self.engine = MultiAgentEngine(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_01_learner_profile_seeded(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM learners WHERE id = 'deeksha'")
        learner = cursor.fetchone()
        self.assertIsNotNone(learner)
        self.assertEqual(learner["name"], "Deeksha")
        self.assertEqual(learner["career_goal"], "Full Stack Developer")
        self.assertEqual(learner["readiness_score"], 42)
        print("✓ Test 1: Deeksha profile seeded with 42% initial career readiness.")

    def test_02_career_dna_seeded(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM career_dna WHERE learner_id = 'deeksha'")
        dna = cursor.fetchone()
        self.assertIsNotNone(dna)
        self.assertGreater(dna["analytical_depth"], 70)
        self.assertGreater(dna["debugging_resilience"], 70)
        strengths = json.loads(dna["natural_strengths"])
        self.assertGreaterEqual(len(strengths), 3)
        print(f"✓ Test 2: Career DNA initialized with {len(strengths)} natural strengths.")

    def test_03_skill_analyzer_audit(self):
        report = self.engine.run_skill_analyzer("deeksha")
        self.assertIn("Python", report["strengths"])
        self.assertIn("SQL", report["strengths"])
        self.assertIn("CSS", report["critical_gaps"])
        self.assertIn("JavaScript", report["critical_gaps"])
        print(f"✓ Test 3: Skill Analyzer audited {report['total_tracked']} skills, confirmed {len(report['strengths'])} strengths and {len(report['critical_gaps'])} critical gaps.")

    def test_04_career_guide_readiness_calculation(self):
        guide = self.engine.run_career_guide("deeksha")
        self.assertEqual(guide["career_goal"], "Full Stack Developer")
        self.assertGreater(guide["readiness_score"], 25)
        self.assertGreater(len(guide["missing_skills"]), 3)
        print(f"✓ Test 4: Career Guide calibrated Career Readiness at {guide['readiness_score']}%.")

    def test_05_learning_planner_4_stages(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM roadmap_stages WHERE learner_id = 'deeksha' ORDER BY stage_number ASC")
        stages = [dict(s) for s in cursor.fetchall()]
        self.assertEqual(len(stages), 4)
        stage_keys = [s["stage_key"] for s in stages]
        self.assertEqual(stage_keys, ["discover", "develop", "create", "achieve"])
        print(f"✓ Test 5: Learning Planner confirmed 4 stages: {', '.join([s['title'] for s in stages])}.")

    def test_06_smart_adapt_ai_low_score_remedial(self):
        # Deliberately fail assessment
        wrong_answers = {"qd_1": 0, "qd_2": 0, "qd_3": 0, "qd_4": 0, "qd_5": 1}
        result = self.engine.evaluate_assessment("deeksha", "quiz_discover", wrong_answers)
        self.assertLess(result["percentage"], 50)
        self.assertEqual(result["smart_adapt_action"], "SMART_ADAPT_REMEDIAL")

        # Verify remedial micro-drill inserted into roadmap
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM roadmap_items WHERE is_adaptive_remedial = 1")
        item = cursor.fetchone()
        self.assertIsNotNone(item)
        self.assertIn("Smart Adapt Drill", item["title"])
        print(f"✓ Test 6: Smart Adapt AI triggered remedial micro-drill on score {result['percentage']}%.")

    def test_07_smart_adapt_ai_high_score_fast_track(self):
        # Ace the assessment
        correct_answers = {"qd_1": 1, "qd_2": 1, "qd_3": 2, "qd_4": 1, "qd_5": 0}
        result = self.engine.evaluate_assessment("deeksha", "quiz_discover", correct_answers)
        self.assertGreaterEqual(result["percentage"], 85)
        self.assertEqual(result["smart_adapt_action"], "SMART_ADAPT_FAST_TRACK")

        # Verify fast-track elective inserted into roadmap
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM roadmap_items WHERE is_adaptive_fasttrack = 1")
        item = cursor.fetchone()
        self.assertIsNotNone(item)
        self.assertIn("Fast-Track Elective", item["title"])
        print(f"✓ Test 7: Smart Adapt AI unlocked Fast-Track elective on score {result['percentage']}%.")

    def test_08_skill_to_project_bridge_evaluation(self):
        calculator_code = """
        class Calculator {
            constructor() { this.currentValue = '0'; this.previousValue = null; }
            appendNumber(num) { this.currentValue += num; }
            chooseOperation(op) { this.operation = op; }
            compute() {
                const prev = parseFloat(this.previousValue);
                const current = parseFloat(this.currentValue);
                switch(this.operation) {
                    case '+': return prev + current;
                }
            }
            clear() { this.currentValue = '0'; }
        }
        """
        result = self.engine.evaluate_project("deeksha", "project_calculator", calculator_code)
        self.assertTrue(result["passed"])
        self.assertGreaterEqual(result["score"], 60)

        # Check skill upgrade in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM skills WHERE learner_id = 'deeksha' AND name LIKE '%JavaScript%'")
        skill = cursor.fetchone()
        self.assertEqual(skill["state"], "mastered")
        print(f"✓ Test 8: Skill-to-Project Bridge evaluated successfully ({result['score']}%) and upgraded JavaScript skill to mastered.")

    def test_09_ai_mentor_chat(self):
        reply = self.engine.chat_with_mentor("deeksha", "What is my next step in the learning journey?")
        self.assertIn("Learning Planner Agent", reply["responder"])
        self.assertIn("Stage 1", reply["message"])
        print(f"✓ Test 9: AI Mentor routed prompt to {reply['responder']} with context-aware advice.")

    def test_10_5_agent_collaborative_huddle(self):
        huddle = self.engine.trigger_agent_collaboration("deeksha")
        self.assertTrue(huddle["success"])
        self.assertEqual(len(huddle["huddle_flow"]), 5)
        print("✓ Test 10: 5-Agent Collaborative Huddle synchronized all 5 agents successfully.")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkilloraAI)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
