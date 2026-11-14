"""
Skillora AI - Database Layer and Domain Schema
Persistent SQLite storage for:
- Learner Profile & Career Ambitions
- Career DNA Dimensions & Strength Diagnostics
- My Skill Universe Graph & Prerequisites
- 4-Stage Learning Journey (Discover, Develop, Create, Achieve)
- Skill-to-Project Bridge (Mini-projects with automated evaluation)
- 5-Agent Multi-Agent Reasoning Logs
- Smart Adapt AI Assessments & Milestones
"""

import sqlite3
import json
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skillora.db")

# Industry Career Benchmarks for Intelligent Matching
CAREER_BENCHMARKS = {
    "Full Stack Developer": {
        "title": "Full Stack Developer",
        "description": "Architects dynamic user experiences, robust microservices, real-time APIs, and scalable relational/NoSQL datastores.",
        "market_demand": "Very High",
        "avg_salary_range": "$95,000 - $145,000",
        "core_competencies": [
            {"name": "HTML5 & Semantic Web", "importance": "High", "target": 85, "category": "Frontend"},
            {"name": "CSS3 & Modern Layouts", "importance": "Critical", "target": 80, "category": "Frontend"},
            {"name": "JavaScript (ES6+)", "importance": "Critical", "target": 90, "category": "Frontend"},
            {"name": "React & Modern UI", "importance": "Critical", "target": 85, "category": "Frontend"},
            {"name": "Node.js & Express", "importance": "Critical", "target": 85, "category": "Backend"},
            {"name": "API Integration (REST & GraphQL)", "importance": "Critical", "target": 85, "category": "Backend"},
            {"name": "SQL & Relational Databases", "importance": "High", "target": 75, "category": "Database"},
            {"name": "Python Fundamentals", "importance": "Medium", "target": 70, "category": "Backend"},
            {"name": "Git & Collaborative Workflows", "importance": "High", "target": 75, "category": "DevOps"},
            {"name": "Web Security & Authentication", "importance": "High", "target": 80, "category": "Security"}
        ]
    },
    "Data Scientist & AI Specialist": {
        "title": "Data Scientist & AI Specialist",
        "description": "Transforms high-dimensional data into strategic value using predictive statistical modeling, PyTorch/TensorFlow, and production RAG pipelines.",
        "market_demand": "High",
        "avg_salary_range": "$105,000 - $160,000",
        "core_competencies": [
            {"name": "Python (Pandas, NumPy, Scikit)", "importance": "Critical", "target": 95, "category": "Core"},
            {"name": "SQL & Data Wrangling", "importance": "Critical", "target": 90, "category": "Database"},
            {"name": "Statistical Inference & Math", "importance": "Critical", "target": 85, "category": "Math"},
            {"name": "Machine Learning Algorithms", "importance": "Critical", "target": 85, "category": "AI"},
            {"name": "Data Visualization (Tableau/Plotly)", "importance": "High", "target": 80, "category": "Analytics"},
            {"name": "Deep Learning (PyTorch)", "importance": "High", "target": 80, "category": "AI"},
            {"name": "LLM Engineering & RAG", "importance": "High", "target": 80, "category": "Generative AI"},
            {"name": "Git & MLOps Pipelines", "importance": "Medium", "target": 70, "category": "DevOps"}
        ]
    },
    "Cloud & DevOps Engineer": {
        "title": "Cloud & DevOps Engineer",
        "description": "Engineers reliable, secure cloud infrastructure, container orchestration, and continuous deployment automated pipelines.",
        "market_demand": "Very High",
        "avg_salary_range": "$100,000 - $150,000",
        "core_competencies": [
            {"name": "Linux Systems & Bash", "importance": "Critical", "target": 90, "category": "Core"},
            {"name": "Docker Containerization", "importance": "Critical", "target": 90, "category": "DevOps"},
            {"name": "Kubernetes Orchestration", "importance": "Critical", "target": 85, "category": "DevOps"},
            {"name": "Cloud Platforms (AWS / GCP)", "importance": "Critical", "target": 85, "category": "Cloud"},
            {"name": "CI/CD (GitHub Actions)", "importance": "High", "target": 85, "category": "DevOps"},
            {"name": "Infrastructure as Code (Terraform)", "importance": "High", "target": 80, "category": "Cloud"},
            {"name": "Python / Go Automation", "importance": "Medium", "target": 75, "category": "Backend"},
            {"name": "Monitoring & SRE Observability", "importance": "Medium", "target": 75, "category": "DevOps"}
        ]
    },
    "Product Designer (UI/UX)": {
        "title": "Product Designer (UI/UX)",
        "description": "Crafts intuitive, accessible, and delightful digital interfaces grounded in user research, design systems, and rapid prototyping.",
        "market_demand": "High",
        "avg_salary_range": "$85,000 - $135,000",
        "core_competencies": [
            {"name": "Design Systems & Figma", "importance": "Critical", "target": 95, "category": "Design"},
            {"name": "User Research & Usability Testing", "importance": "Critical", "target": 90, "category": "Research"},
            {"name": "Wireframing & Prototyping", "importance": "Critical", "target": 90, "category": "Design"},
            {"name": "Accessibility Standards (WCAG AAA)", "importance": "High", "target": 85, "category": "Standards"},
            {"name": "Information Architecture", "importance": "High", "target": 85, "category": "Strategy"},
            {"name": "HTML/CSS Fundamentals", "importance": "Medium", "target": 70, "category": "Frontend"},
            {"name": "Interaction Design & Micro-animations", "importance": "Medium", "target": 75, "category": "Design"}
        ]
    }
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed=False):
    conn = get_db()
    cursor = conn.cursor()

    if force_reseed:
        cursor.execute("DROP TABLE IF EXISTS learners")
        cursor.execute("DROP TABLE IF EXISTS career_dna")
        cursor.execute("DROP TABLE IF EXISTS skills")
        cursor.execute("DROP TABLE IF EXISTS roadmap_stages")
        cursor.execute("DROP TABLE IF EXISTS roadmap_items")
        cursor.execute("DROP TABLE IF EXISTS skill_projects")
        cursor.execute("DROP TABLE IF EXISTS agent_exchange_logs")
        cursor.execute("DROP TABLE IF EXISTS assessments")
        cursor.execute("DROP TABLE IF EXISTS milestones")

    # 1. Learner Profile
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learners (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        headline TEXT,
        bio TEXT,
        career_goal TEXT NOT NULL,
        secondary_interest TEXT,
        readiness_score INTEGER DEFAULT 0,
        skill_strength INTEGER DEFAULT 0,
        learning_streak INTEGER DEFAULT 1,
        weekly_hours REAL DEFAULT 0.0,
        daily_goal TEXT,
        daily_goal_completed INTEGER DEFAULT 0,
        smart_adapt_active INTEGER DEFAULT 0,
        smart_adapt_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Career DNA Dimensions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_dna (
        learner_id TEXT PRIMARY KEY,
        analytical_depth INTEGER DEFAULT 75,
        system_thinking INTEGER DEFAULT 80,
        creative_iteration INTEGER DEFAULT 70,
        execution_velocity INTEGER DEFAULT 65,
        debugging_resilience INTEGER DEFAULT 85,
        architecture_vision INTEGER DEFAULT 60,
        natural_strengths TEXT, -- JSON array
        growth_edges TEXT,      -- JSON array
        recommended_paths TEXT, -- JSON array
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    # 3. My Skill Universe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id TEXT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        proficiency INTEGER DEFAULT 0,
        state TEXT NOT NULL, -- 'mastered', 'learning', 'missing', 'recommended'
        importance TEXT DEFAULT 'Medium', -- 'Critical', 'High', 'Medium'
        prerequisites TEXT, -- JSON array of skill names
        resources TEXT,     -- JSON array of resource links
        universe_x INTEGER DEFAULT 50, -- Graph coordinate percent
        universe_y INTEGER DEFAULT 50,
        connections TEXT,   -- JSON array of connected skill names
        notes TEXT,
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    # 4. Roadmap Stages (Discover, Develop, Create, Achieve)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_stages (
        id TEXT PRIMARY KEY,
        learner_id TEXT,
        stage_key TEXT NOT NULL, -- 'discover', 'develop', 'create', 'achieve'
        stage_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        tagline TEXT NOT NULL,
        description TEXT NOT NULL,
        duration_hours INTEGER DEFAULT 20,
        status TEXT DEFAULT 'pending', -- 'active', 'pending', 'completed'
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    # 5. Roadmap Items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_items (
        id TEXT PRIMARY KEY,
        stage_id TEXT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        item_type TEXT NOT NULL, -- 'concept', 'drill', 'quiz', 'project', 'remedial', 'advanced'
        estimated_time TEXT,
        completed INTEGER DEFAULT 0,
        is_adaptive_remedial INTEGER DEFAULT 0,
        is_adaptive_fasttrack INTEGER DEFAULT 0,
        resource_label TEXT,
        resource_url TEXT,
        FOREIGN KEY (stage_id) REFERENCES roadmap_stages(id)
    )
    """)

    # 6. Skill-to-Project Bridge
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skill_projects (
        id TEXT PRIMARY KEY,
        learner_id TEXT,
        title TEXT NOT NULL,
        associated_skill TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        scenario TEXT NOT NULL,
        objectives TEXT, -- JSON array
        starter_code TEXT NOT NULL,
        solution_keywords TEXT, -- JSON array
        status TEXT DEFAULT 'assigned', -- 'assigned', 'in_progress', 'completed'
        score INTEGER DEFAULT 0,
        feedback TEXT,
        completed_at TIMESTAMP,
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    # 7. Multi-Agent Structured Exchange Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_exchange_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id TEXT,
        agent_name TEXT NOT NULL,
        agent_role TEXT NOT NULL,
        target_agent TEXT,
        action TEXT NOT NULL,
        message TEXT NOT NULL,
        payload TEXT, -- JSON
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    # 8. Assessments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id TEXT PRIMARY KEY,
        learner_id TEXT,
        quiz_id TEXT NOT NULL,
        quiz_title TEXT NOT NULL,
        score INTEGER NOT NULL,
        max_score INTEGER NOT NULL,
        percentage INTEGER NOT NULL,
        smart_adapt_action TEXT,
        struggles_identified TEXT, -- JSON array
        taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    # 9. Milestones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS milestones (
        id TEXT PRIMARY KEY,
        learner_id TEXT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        icon TEXT NOT NULL,
        achieved INTEGER DEFAULT 0,
        achieved_at TIMESTAMP,
        FOREIGN KEY (learner_id) REFERENCES learners(id)
    )
    """)

    conn.commit()

    # Seed Deeksha profile if table is empty or forced
    cursor.execute("SELECT COUNT(*) as count FROM learners WHERE id = 'deeksha'")
    if cursor.fetchone()["count"] == 0:
        seed_deeksha_profile(conn)

    conn.close()

def seed_deeksha_profile(conn):
    cursor = conn.cursor()

    # 1. Learner Profile
    cursor.execute("""
    INSERT INTO learners (
        id, name, email, headline, bio, career_goal, secondary_interest,
        readiness_score, skill_strength, learning_streak, weekly_hours,
        daily_goal, daily_goal_completed, smart_adapt_active, smart_adapt_reason
    ) VALUES (
        'deeksha',
        'Deeksha',
        'deeksha@skillora.ai',
        'Aspiring Full Stack Engineer & Creative Builder',
        'Passionate computer science learner transitioning foundational algorithmic skills in Python and SQL into production full-stack web and API architectures.',
        'Full Stack Developer',
        'Human-Centered Design & Distributed Systems',
        42,
        45,
        6,
        5.5,
        'Master CSS Flexbox layouts & ES6 JavaScript arrow functions',
        0,
        0,
        'Initial baseline calibrated by Skill Analyzer and Career Guide Agents.'
    )
    """)

    # 2. Career DNA
    natural_strengths = [
        "Structured Relational Thinking (Strong SQL foundations)",
        "Backend Scripting & Automation (Proficient in Python)",
        "Systematic Root-Cause Debugging",
        "High Learning Agility & Conceptual Curiosity"
    ]
    growth_edges = [
        "Visual Layout Execution (CSS Box Model & Flexbox)",
        "Client-Side Asynchronous State (JS Promises & Event Loop)",
        "Component Lifecycle & State Management (React Hooks)",
        "Production RESTful Endpoints & Express Routing"
    ]
    recommended_paths = [
        {"role": "Full Stack Developer", "fit_score": 92, "reason": "Direct synergy between your Python/SQL logic and modern web frameworks."},
        {"role": "Backend API Engineer", "fit_score": 88, "reason": "Your analytical rigor maps naturally to microservices and database design."},
        {"role": "Data Systems Engineer", "fit_score": 82, "reason": "Strong data manipulation aptitude with room for real-time pipelines."}
    ]
    cursor.execute("""
    INSERT INTO career_dna (
        learner_id, analytical_depth, system_thinking, creative_iteration,
        execution_velocity, debugging_resilience, architecture_vision,
        natural_strengths, growth_edges, recommended_paths
    ) VALUES (
        'deeksha',
        82, 78, 68, 72, 85, 64,
        ?, ?, ?
    )
    """, (json.dumps(natural_strengths), json.dumps(growth_edges), json.dumps(recommended_paths)))

    # 3. My Skill Universe Nodes (Coordinates for visual galaxy / constellation)
    skills_data = [
        # Mastered
        ("deeksha", "Python", "Backend", 70, "mastered", "High",
         json.dumps(["Basic Computer Science"]),
         json.dumps([{"title": "Python Docs", "url": "https://docs.python.org/3/"}, {"title": "Real Python", "url": "https://realpython.com"}]),
         28, 35, json.dumps(["SQL", "Node.js", "API Integration"]),
         "Strong foundational grasp of OOP, collections, list comprehensions, and clean scripting."),

        ("deeksha", "SQL", "Database", 65, "mastered", "High",
         json.dumps(["Relational Tables"]),
         json.dumps([{"title": "PostgreSQL Tutorial", "url": "https://postgresqltutorial.com"}, {"title": "Mode SQL School", "url": "https://mode.com/sql-tutorial"}]),
         42, 28, json.dumps(["Python", "API Integration", "Database Design"]),
         "Confident in multi-table JOINs, GROUP BY aggregations, subqueries, and table schema definitions."),

        # Currently Learning
        ("deeksha", "Basic HTML", "Frontend", 50, "learning", "High",
         json.dumps(["Web Basics"]),
         json.dumps([{"title": "MDN HTML5 Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML"}, {"title": "web.dev Semantics", "url": "https://web.dev/learn/html"}]),
         55, 42, json.dumps(["CSS", "JavaScript"]),
         "Understands tags, forms, input types, and attributes. Currently adopting modern semantic elements (nav, main, article)."),

        # Missing Skills (Identified Learning Needs)
        ("deeksha", "CSS", "Frontend", 15, "missing", "Critical",
         json.dumps(["Basic HTML"]),
         json.dumps([{"title": "CSS-Tricks Flexbox Guide", "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/"}, {"title": "Flexbox Froggy", "url": "https://flexboxfroggy.com"}]),
         70, 36, json.dumps(["Basic HTML", "React", "JavaScript"]),
         "Immediate gap: Modern Flexbox axis alignment, CSS Grid 2D layouts, and responsive media query breakpoints."),

        ("deeksha", "JavaScript", "Frontend", 10, "missing", "Critical",
         json.dumps(["Basic HTML", "CSS"]),
         json.dumps([{"title": "JavaScript.info", "url": "https://javascript.info"}, {"title": "MDN JavaScript Core", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"}]),
         68, 56, json.dumps(["CSS", "React", "Node.js", "API Integration"]),
         "Critical gap: ES6+ arrow functions, closures, DOM manipulation, promises, async/await, and microtask queues."),

        ("deeksha", "React", "Frontend", 0, "missing", "Critical",
         json.dumps(["JavaScript", "CSS"]),
         json.dumps([{"title": "React Official Docs", "url": "https://react.dev"}, {"title": "React Hooks Explained", "url": "https://react.dev/reference/react"}]),
         82, 50, json.dumps(["JavaScript", "CSS", "API Integration"]),
         "Key goal: Component architecture, unidirectional state props, useState/useEffect hooks, and declarative UI rendering."),

        ("deeksha", "Node.js", "Backend", 0, "missing", "Critical",
         json.dumps(["JavaScript"]),
         json.dumps([{"title": "Node.js Core Architecture", "url": "https://nodejs.org/en/learn"}, {"title": "Express.js Routing Guide", "url": "https://expressjs.com"}]),
         52, 68, json.dumps(["JavaScript", "SQL", "API Integration"]),
         "Essential backend runtime: Event Loop, npm packages, Express HTTP routers, and middleware request-response pipelines."),

        ("deeksha", "API Integration", "Backend", 5, "missing", "Critical",
         json.dumps(["JavaScript", "Node.js", "SQL"]),
         json.dumps([{"title": "RESTful API Architectural Constraints", "url": "https://restfulapi.net"}, {"title": "Postman API Foundations", "url": "https://postman.com"}]),
         66, 75, json.dumps(["Node.js", "React", "SQL"]),
         "Synthesizing client and server: JSON serialization, HTTP headers, CORS, JWT authentication, and fetch error boundaries."),

        # Recommended Next Skills
        ("deeksha", "Git & GitHub", "DevOps", 48, "recommended", "High",
         json.dumps(["Terminal CLI"]),
         json.dumps([{"title": "Pro Git Book", "url": "https://git-scm.com/book/en/v2"}, {"title": "GitHub Skills", "url": "https://skills.github.com"}]),
         35, 62, json.dumps(["Python", "JavaScript"]),
         "Recommended for professional teamwork: Branching, merging, pull requests, resolving conflicts, and CI status checks."),

        ("deeksha", "Web Security Basics", "Security", 20, "recommended", "High",
         json.dumps(["API Integration"]),
         json.dumps([{"title": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/"}]),
         80, 78, json.dumps(["API Integration", "Node.js"]),
         "Preventing SQL injection via parameterized queries, XSS mitigation with CSP headers, and password hashing with bcrypt.")
    ]

    cursor.executemany("""
    INSERT INTO skills (
        learner_id, name, category, proficiency, state, importance,
        prerequisites, resources, universe_x, universe_y, connections, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, skills_data)

    # 4. 4-Stage Learning Journey
    stages = [
        ("stage_discover", "deeksha", "discover", 1, "Stage 1: Discover", "Uncover Foundations & Mental Models",
         "Deconstruct web architecture, explore semantic HTML5 structure, and master modern CSS visual layout mechanics.", 24, "active"),
        ("stage_develop", "deeksha", "develop", 2, "Stage 2: Develop", "Build Essential Technical Execution",
         "Deep-dive into modern JavaScript ES6+, reactive component architecture with React, and asynchronous server runtimes with Node.js.", 36, "pending"),
        ("stage_create", "deeksha", "create", 3, "Stage 3: Create", "Complete Practical Real-World Projects",
         "Architect and deliver working applications: Interactive Calculator, Developer Portfolio, REST API Service, and Relational Database.", 42, "pending"),
        ("stage_achieve", "deeksha", "achieve", 4, "Stage 4: Achieve", "Demonstrate Career Readiness & Impact",
         "End-to-end cloud deployment, CI/CD pipelines, security hardening, performance profiling, and simulated hiring interviews.", 20, "pending")
    ]
    cursor.executemany("""
    INSERT INTO roadmap_stages (id, learner_id, stage_key, stage_number, title, tagline, description, duration_hours, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, stages)

    # Roadmap Items
    items_discover = [
        ("item_d1", "stage_discover", "Semantic HTML5 Architecture & Screen Reader A11y",
         "Structure modern web documents with header, nav, main, section, and adhere to WCAG accessibility principles.", "concept", "2.5 hrs", 1, 0, 0, "MDN Semantic Web", "https://developer.mozilla.org/en-US/docs/Glossary/Semantics#semantics_in_html"),
        ("item_d2", "stage_discover", "CSS Box Model & Fluid Typography Foundations",
         "Master margins, padding, border-box sizing, viewport units, and modular CSS variables.", "concept", "3 hrs", 1, 0, 0, "web.dev CSS Box Model", "https://web.dev/learn/css/box-model/"),
        ("item_d3", "stage_discover", "Interactive CSS Flexbox Mastery Drills",
         "Build responsive card grids, navigation bars, and alignment controls using flex-direction, justify-content, and align-items.", "drill", "3.5 hrs", 0, 0, 0, "Flexbox Froggy Challenge", "https://flexboxfroggy.com"),
        ("item_d4", "stage_discover", "CSS Grid 2D Layouts & Responsive Breakpoints",
         "Design editorial magazine layouts and responsive dashboard viewports without media query bloat.", "drill", "4 hrs", 0, 0, 0, "CSS Grid Garden", "https://cssgridgarden.com"),
        ("item_d5", "stage_discover", "Foundational Diagnostics & Web Architecture Quiz",
         "Adaptive assessment evaluating semantic markup, layout rendering pipelines, and DOM structure.", "quiz", "30 mins", 0, 0, 0, "Stage 1 Diagnostic Quiz", "quiz_discover")
    ]
    cursor.executemany("""
    INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items_discover)

    items_develop = [
        ("item_dev1", "stage_develop", "JavaScript ES6+ Syntax, Scoping & Closures",
         "Master arrow functions, object destructuring, rest/spread operators, let/const lexical scoping, and execution contexts.", "concept", "4.5 hrs", 0, 0, 0, "JavaScript.info Closures", "https://javascript.info/closure"),
        ("item_dev2", "stage_develop", "Asynchronous JavaScript: Promises & Event Loop",
         "Deconstruct microtasks vs macrotasks, async/await error propagation, and real-time fetch streams.", "concept", "5 hrs", 0, 0, 0, "MDN Async JS", "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous"),
        ("item_dev3", "stage_develop", "React Declarative Components, Props & Hooks",
         "Compose reusable component trees, manage reactive state with useState, and orchestrate side effects with useEffect.", "drill", "6.5 hrs", 0, 0, 0, "React.dev Hooks Guide", "https://react.dev/learn"),
        ("item_dev4", "stage_develop", "Node.js Runtime Architecture & Express Routing",
         "Spin up HTTP servers, implement modular middleware pipelines, parse incoming request bodies, and handle errors gracefully.", "drill", "6 hrs", 0, 0, 0, "Express.js Guide", "https://expressjs.com"),
        ("item_dev5", "stage_develop", "Stage 2 Mid-Flight Adaptive Evaluation",
         "Interactive coding assessment analyzing React hook rules, closure scoping, and Express request flows.", "quiz", "45 mins", 0, 0, 0, "Stage 2 Comprehensive Assessment", "quiz_develop")
    ]
    cursor.executemany("""
    INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items_develop)

    items_create = [
        ("item_c1", "stage_create", "Skill-to-Project Bridge: Interactive Calculator",
         "Implement a clean JavaScript stateful calculator handling decimals, operator precedence, and keyboard events.", "project", "5 hrs", 0, 0, 0, "Project Bridge Lab", "project_calculator"),
        ("item_c2", "stage_create", "Skill-to-Project Bridge: Developer Portfolio in React",
         "Craft an accessible, responsive personal portfolio with theme toggling, component modals, and interactive project showcases.", "project", "8 hrs", 0, 0, 0, "Project Bridge Lab", "project_portfolio"),
        ("item_c3", "stage_create", "Skill-to-Project Bridge: Node.js Backend API Service",
         "Build a secure RESTful API endpoint suite with input validation, JWT token signing, and JSON responses.", "project", "9 hrs", 0, 0, 0, "Project Bridge Lab", "project_backend_api"),
        ("item_c4", "stage_create", "Skill-to-Project Bridge: Relational Database Design",
         "Design a normalized schema (3NF) for an e-commerce platform with indexing, foreign keys, and complex aggregate queries.", "project", "7 hrs", 0, 0, 0, "Project Bridge Lab", "project_database")
    ]
    cursor.executemany("""
    INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items_create)

    items_achieve = [
        ("item_a1", "stage_achieve", "Docker Containerization & Multi-Stage Production Builds",
         "Write slim Alpine Dockerfiles for frontend and backend with isolated environment variables.", "drill", "4 hrs", 0, 0, 0, "Docker Best Practices", "https://docs.docker.com"),
        ("item_a2", "stage_achieve", "Automated CI/CD Pipeline with GitHub Actions",
         "Automate automated testing, lint validation, security vulnerability scanning, and cloud deployment.", "drill", "4.5 hrs", 0, 0, 0, "GitHub Actions Docs", "https://docs.github.com/actions"),
        ("item_a3", "stage_achieve", "Web Performance Optimization & Lighthouse 95+ Audit",
         "Eliminate render-blocking CSS, configure asset compression, bundle splitting, and optimize Core Web Vitals.", "concept", "3.5 hrs", 0, 0, 0, "web.dev Vitals", "https://web.dev/vitals/"),
        ("item_a4", "stage_achieve", "Full Stack Simulated Technical Interview",
         "Comprehensive real-world scenario interview with coding challenge, system architecture defense, and behavioral questions.", "quiz", "2 hrs", 0, 0, 0, "Final Career Simulation", "quiz_achieve")
    ]
    cursor.executemany("""
    INSERT INTO roadmap_items (id, stage_id, title, description, item_type, estimated_time, completed, is_adaptive_remedial, is_adaptive_fasttrack, resource_label, resource_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items_achieve)

    # 5. Skill-to-Project Bridge (Mini-Projects for missing skills)
    projects_data = [
        (
            "project_calculator",
            "deeksha",
            "JavaScript Interactive Calculator",
            "JavaScript",
            "Beginner-Intermediate",
            "Build an interactive mathematical calculator component that supports addition, subtraction, multiplication, division, decimal chaining, and clear state recovery.",
            json.dumps(["Implement `calculate(op1, op2, operator)`", "Support continuous operand chaining", "Prevent division by zero with error message", "Maintain clean state object"]),
            """// Skillora Skill-to-Project Bridge: Interactive Calculator
// Target Skill: JavaScript (ES6+ State & Logic)

class Calculator {
    constructor() {
        this.currentValue = '0';
        this.previousValue = null;
        this.operation = null;
        this.shouldResetScreen = false;
    }

    appendNumber(number) {
        if (this.currentValue === '0' || this.shouldResetScreen) {
            this.currentValue = number.toString();
            this.shouldResetScreen = false;
        } else {
            if (number === '.' && this.currentValue.includes('.')) return;
            this.currentValue += number.toString();
        }
    }

    chooseOperation(operation) {
        if (this.previousValue !== null) {
            this.compute();
        }
        this.operation = operation;
        this.previousValue = this.currentValue;
        this.shouldResetScreen = true;
    }

    compute() {
        const prev = parseFloat(this.previousValue);
        const current = parseFloat(this.currentValue);
        if (isNaN(prev) || isNaN(current)) return;

        let result;
        switch (this.operation) {
            case '+': result = prev + current; break;
            case '-': result = prev - current; break;
            case '*': result = prev * current; break;
            case '/': 
                if (current === 0) {
                    this.currentValue = 'Error: Div by 0';
                    this.operation = null;
                    this.previousValue = null;
                    return;
                }
                result = prev / current; 
                break;
            default: return;
        }

        this.currentValue = Math.round(result * 100000) / 100000;
        this.operation = null;
        this.previousValue = null;
        this.shouldResetScreen = true;
    }

    clear() {
        this.currentValue = '0';
        this.previousValue = null;
        this.operation = null;
    }
}
""",
            json.dumps(["appendNumber", "compute", "chooseOperation", "parseFloat", "currentValue", "switch", "clear"]),
            "assigned",
            0,
            "Awaiting code execution and test runner evaluation.",
            None
        ),
        (
            "project_portfolio",
            "deeksha",
            "Developer Portfolio Component",
            "React",
            "Intermediate",
            "Construct a dynamic React developer profile component featuring skill badge rendering, dynamic project filtering by tech stack, and interactive contact modal state.",
            json.dumps(["Build modular `ProjectCard` and `SkillBadge` sub-components", "Implement filter state by category (Frontend, Backend, Database)", "Integrate clean prop interfaces and key attributes", "Support theme toggle state"]),
            """// Skillora Skill-to-Project Bridge: React Developer Portfolio
// Target Skill: React Components & Reactive State

function Portfolio({ learnerName, role, skills, projects }) {
    const [selectedCategory, setSelectedCategory] = React.useState('All');
    const [contactOpen, setContactOpen] = React.useState(false);

    const filteredProjects = selectedCategory === 'All'
        ? projects
        : projects.filter(p => p.category === selectedCategory);

    return (
        <div className="portfolio-container">
            <header className="portfolio-hero">
                <h1>{learnerName}</h1>
                <p className="subtitle">{role}</p>
                <button onClick={() => setContactOpen(true)} className="btn-contact">
                    Get In Touch
                </button>
            </header>

            <section className="skills-belt">
                <h3>Verified Competencies</h3>
                <div className="badge-grid">
                    {skills.map(s => (
                        <span key={s.name} className={`badge badge-${s.state}`}>
                            {s.name} ({s.proficiency}%)
                        </span>
                    ))}
                </div>
            </section>

            <section className="projects-grid">
                {filteredProjects.map(proj => (
                    <article key={proj.id} className="project-card">
                        <h4>{proj.title}</h4>
                        <p>{proj.description}</p>
                        <span className="tag">{proj.category}</span>
                    </article>
                ))}
            </section>
        </div>
    );
}
""",
            json.dumps(["React.useState", "filteredProjects", "selectedCategory", "map", "key=", "skills.map", "className"]),
            "assigned",
            0,
            "Awaiting submission.",
            None
        ),
        (
            "project_backend_api",
            "deeksha",
            "Express & Node.js RESTful API",
            "Node.js & Express",
            "Intermediate",
            "Implement a production-structured Express router featuring GET /api/learners, POST /api/skills with input sanitization, and standardized JSON error formatting.",
            json.dumps(["Configure express.Router() with modular handlers", "Implement request body validation for skill name and proficiency (0-100)", "Return appropriate HTTP status codes (200, 201, 400, 404)", "Include CORS and JSON headers"]),
            """// Skillora Skill-to-Project Bridge: Node.js & Express REST API
// Target Skill: Node.js Backend & API Routing

const express = require('express');
const router = express.Router();

// Mock store
let skillsDb = [
    { id: 1, name: 'Python', category: 'Backend', proficiency: 70 },
    { id: 2, name: 'SQL', category: 'Database', proficiency: 65 }
];

router.get('/api/skills', (req, res) => {
    res.status(200).json({ success: true, count: skillsDb.length, data: skillsDb });
});

router.post('/api/skills', (req, res) => {
    const { name, category, proficiency } = req.body;
    
    // Strict input validation
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
        return res.status(400).json({ success: false, error: 'Valid skill name required.' });
    }
    
    const profNum = parseInt(proficiency, 10);
    if (isNaN(profNum) || profNum < 0 || profNum > 100) {
        return res.status(400).json({ success: false, error: 'Proficiency must be an integer between 0 and 100.' });
    }

    const newSkill = {
        id: skillsDb.length + 1,
        name: name.trim(),
        category: category || 'General',
        proficiency: profNum
    };

    skillsDb.push(newSkill);
    return res.status(201).json({ success: true, data: newSkill });
});

module.exports = router;
""",
            json.dumps(["express.Router()", "router.get", "router.post", "res.status(200)", "res.status(201)", "res.status(400)", "req.body"]),
            "assigned",
            0,
            "Awaiting evaluation.",
            None
        ),
        (
            "project_database",
            "deeksha",
            "Relational Database Schema & Query Engine",
            "SQL & Relational Databases",
            "Intermediate",
            "Draft a 3NF normalized schema for a learning platform (learners, courses, enrollments) and write analytical window queries calculating learner completion rates.",
            json.dumps(["Write DDL CREATE TABLE with primary and foreign keys", "Enforce UNIQUE and NOT NULL constraints", "Write aggregate query calculating completion % per course", "Use JOIN and CASE WHEN logic"]),
            """-- Skillora Skill-to-Project Bridge: Database Schema & Analytics
-- Target Skill: Relational Database Modeling & Window Queries

CREATE TABLE IF NOT EXISTS learners (
    learner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    joined_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    difficulty TEXT CHECK (difficulty IN ('Beginner', 'Intermediate', 'Advanced'))
);

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    learner_id INTEGER REFERENCES learners(learner_id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    progress_pct INTEGER DEFAULT 0 CHECK (progress_pct BETWEEN 0 AND 100),
    completed_at TIMESTAMP
);

-- Analytical Query: Course Performance & Completion Velocity
SELECT 
    c.title AS course_title,
    COUNT(e.enrollment_id) AS total_enrolled,
    ROUND(AVG(e.progress_pct), 1) AS avg_progress_percent,
    SUM(CASE WHEN e.progress_pct = 100 THEN 1 ELSE 0 END) AS fully_graduated_count,
    ROUND(SUM(CASE WHEN e.progress_pct = 100 THEN 1.0 ELSE 0.0 END) / COUNT(e.enrollment_id) * 100, 1) AS graduation_rate_pct
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.title
ORDER BY total_enrolled DESC;
""",
            json.dumps(["CREATE TABLE", "PRIMARY KEY", "FOREIGN KEY", "REFERENCES", "SELECT", "AVG", "CASE WHEN", "GROUP BY"]),
            "assigned",
            0,
            "Awaiting evaluation.",
            None
        )
    ]
    cursor.executemany("""
    INSERT INTO skill_projects (
        id, learner_id, title, associated_skill, difficulty, scenario,
        objectives, starter_code, solution_keywords, status, score, feedback, completed_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, projects_data)

    # 6. Multi-Agent Reasoning Exchange Logs (Structured collaboration)
    initial_agent_logs = [
        ("deeksha", "Skill Analyzer Agent", "Skill Discovery", "Career Guide Agent", "SKILL_AUDIT_COMPLETE",
         "Audited Deeksha's GitHub submissions & past coursework. Identified strong Python (70%) and SQL (65%) competencies. Discovered critical unvalidated gaps: CSS (15%), JavaScript (10%), React (0%), Node.js (0%), API Integration (5%).",
         json.dumps({"strengths": ["Python", "SQL"], "gaps": ["CSS", "JavaScript", "React", "Node.js", "API Integration"], "total_tracked": 10})),

        ("deeksha", "Career Guide Agent", "Benchmark Analysis", "Learning Planner Agent", "READINESS_CALIBRATED",
         "Benchmarked Deeksha against 2026 Full Stack Developer industry criteria. Calculated baseline Career Readiness at 42%. Prioritized essential bridges: CSS layout mechanics and JavaScript async execution before introducing React.",
         json.dumps({"career_goal": "Full Stack Developer", "readiness_score": 42, "critical_gap_count": 5})),

        ("deeksha", "Learning Planner Agent", "Roadmap Synthesis", "Progress Evaluator Agent", "JOURNEY_STRUCTURED",
         "Generated 4-Stage Learning Journey (Discover, Develop, Create, Achieve) spanning 122 total hours. Synchronized 4 hands-on projects directly targeted at missing competencies.",
         json.dumps({"stages": ["Discover", "Develop", "Create", "Achieve"], "projects_assigned": 4})),

        ("deeksha", "Progress Evaluator Agent", "Diagnostic Setup", "AI Mentor Agent", "SMART_ADAPT_INITIALIZED",
         "Smart Adapt AI engine armed. Dynamic thresholds configured: <50% score triggers remedial concept revision without penalty; >85% triggers fast-track elective modules; repeated mistakes isolate targeted practice.",
         json.dumps({"remedial_threshold": 50, "fast_track_threshold": 85, "monitoring": "Active"})),

        ("deeksha", "AI Mentor Agent", "Personalized Guidance", "Deeksha (Learner)", "WELCOME_AND_MISSION",
         "Welcome to Skillora AI, Deeksha! Every skill has a purpose, and your journey toward becoming a Full Stack Developer starts with your strengths. Your daily mission: master CSS Flexbox layout mechanics in Stage 1.",
         json.dumps({"daily_goal": "Master CSS Flexbox layouts & ES6 JavaScript arrow functions", "confidence_forecast": "High"}))
    ]
    cursor.executemany("""
    INSERT INTO agent_exchange_logs (
        learner_id, agent_name, agent_role, target_agent, action, message, payload
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, initial_agent_logs)

    # 7. Milestones
    milestones_data = [
        ("m1", "deeksha", "Curiosity Spark", "Enrolled in Skillora AI and completed initial Career DNA analysis.", "Onboarding", "sparkle", 1, datetime.datetime.now().isoformat()),
        ("m2", "deeksha", "Momentum Builder", "Maintained an active 6-day learning streak without missing a daily mission.", "Consistency", "flame", 1, datetime.datetime.now().isoformat()),
        ("m3", "deeksha", "Diagnostic Vanguard", "Scored 85%+ on any adaptive assessment to unlock Fast-Track privileges.", "Assessment", "target", 0, None),
        ("m4", "deeksha", "Bridge Builder", "Successfully constructed and tested a Skill-to-Project Bridge application.", "Projects", "code", 0, None),
        ("m5", "deeksha", "Full Stack Emergence", "Achieved an 80%+ Career Readiness Score across all 4 stages.", "Career", "trophy", 0, None)
    ]
    cursor.executemany("""
    INSERT INTO milestones (
        id, learner_id, title, description, category, icon, achieved, achieved_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, milestones_data)

    conn.commit()

if __name__ == "__main__":
    init_db(force_reseed=True)
    print("Skillora database initialized and seeded successfully.")
