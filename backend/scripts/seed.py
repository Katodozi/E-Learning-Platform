"""Seed database with expertise, roadmaps, skills, topics, admin, and prompts."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.security import get_password_hash
from app.database.session import SessionLocal
from app.models import Admin, Expertise, PromptTemplate, Roadmap, RoadmapLevel, Skill, Topic
from app.services.gemini.gemini_service import DEFAULT_QUIZ_PROMPT, DEFAULT_SKILL_PROMPT

SEED_EXPERTISE = [
    {
        "name": "Frontend Development",
        "slug": "frontend-development",
        "description": "Build modern, responsive user interfaces with HTML, CSS, JavaScript, and popular frameworks.",
        "icon": "layout",
        "skills_by_level": {
            "beginner": [
                ("HTML Fundamentals", "Learn semantic HTML structure and accessibility basics.", ["Elements & Tags", "Semantic HTML", "Forms", "Accessibility"]),
                ("CSS Basics", "Style web pages with selectors, box model, and layouts.", ["Selectors", "Box Model", "Flexbox", "Responsive Design"]),
                ("JavaScript Essentials", "Core programming concepts for the browser.", ["Variables", "Functions", "DOM Manipulation", "Events"]),
            ],
            "intermediate": [
                ("React", "Build component-based UIs with React.", ["Components", "Props", "State", "Hooks", "Context API"]),
                ("TypeScript", "Add static typing to JavaScript projects.", ["Types", "Interfaces", "Generics", "Type Guards"]),
                ("State Management", "Manage application state effectively.", ["Local State", "Context", "Zustand", "Data Fetching"]),
            ],
            "advanced": [
                ("Performance Optimization", "Optimize frontend performance and Core Web Vitals.", ["Code Splitting", "Lazy Loading", "Memoization", "Bundle Analysis"]),
                ("Testing", "Write reliable frontend tests.", ["Unit Tests", "Integration Tests", "E2E Tests", "Testing Library"]),
                ("Architecture Patterns", "Design scalable frontend architectures.", ["Feature Folders", "Design Systems", "Micro Frontends", "SSR/SSG"]),
            ],
        },
    },
    {
        "name": "Backend Development",
        "slug": "backend-development",
        "description": "Design and build robust server-side applications, APIs, and business logic.",
        "icon": "server",
        "skills_by_level": {
            "beginner": [
                ("HTTP & REST", "Understand web protocols and RESTful API design.", ["HTTP Methods", "Status Codes", "REST Principles", "JSON"]),
                ("Python Basics", "Core Python for backend development.", ["Syntax", "Data Structures", "Functions", "Modules"]),
                ("Databases Intro", "Fundamentals of relational databases.", ["Tables", "Queries", "Relationships", "CRUD"]),
            ],
            "intermediate": [
                ("FastAPI", "Build high-performance APIs with FastAPI.", ["Routing", "Pydantic", "Dependency Injection", "Middleware"]),
                ("SQLAlchemy", "ORM patterns for database access.", ["Models", "Sessions", "Queries", "Relationships"]),
                ("Authentication", "Secure APIs with JWT and password hashing.", ["JWT", "OAuth Basics", "Password Hashing", "Protected Routes"]),
            ],
            "advanced": [
                ("Microservices", "Design distributed backend systems.", ["Service Boundaries", "API Gateway", "Message Queues", "Event-Driven"]),
                ("Caching", "Improve performance with caching strategies.", ["Redis", "Cache Invalidation", "TTL", "Cache-Aside"]),
                ("Observability", "Monitor and debug production systems.", ["Logging", "Metrics", "Tracing", "Alerting"]),
            ],
        },
    },
    {
        "name": "Database Engineering",
        "slug": "database-engineering",
        "description": "Design, optimize, and manage relational and NoSQL database systems.",
        "icon": "database",
        "skills_by_level": {
            "beginner": [
                ("SQL Fundamentals", "Write basic SQL queries and understand schemas.", ["SELECT", "INSERT", "UPDATE", "DELETE"]),
                ("Data Modeling", "Design normalized database schemas.", ["Entities", "Relationships", "Normalization", "Keys"]),
                ("PostgreSQL Basics", "Get started with PostgreSQL.", ["Installation", "psql", "Data Types", "Constraints"]),
            ],
            "intermediate": [
                ("Indexing", "Optimize query performance with indexes.", ["B-Tree Indexes", "Composite Indexes", "Query Plans", "EXPLAIN"]),
                ("Transactions", "Ensure data integrity with ACID transactions.", ["ACID", "Isolation Levels", "Locks", "Deadlocks"]),
                ("Migrations", "Manage schema changes safely.", ["Alembic", "Versioning", "Rollback", "Seed Data"]),
            ],
            "advanced": [
                ("Query Optimization", "Advanced performance tuning techniques.", ["Statistics", "Join Optimization", "Partitioning", "Materialized Views"]),
                ("Replication", "High availability and read scaling.", ["Primary-Replica", "Failover", "Lag Monitoring", "Streaming Replication"]),
                ("Security", "Secure database systems.", ["Roles", "RLS", "Encryption", "Auditing"]),
            ],
        },
    },
    {
        "name": "DevOps",
        "slug": "devops",
        "description": "Automate infrastructure, deployments, and operational workflows.",
        "icon": "cloud",
        "skills_by_level": {
            "beginner": [
                ("Linux Basics", "Essential command-line and file system skills.", ["Shell Commands", "Permissions", "Processes", "Package Managers"]),
                ("Git & Version Control", "Collaborate with Git workflows.", ["Commits", "Branches", "Merge", "Pull Requests"]),
                ("CI/CD Intro", "Understand continuous integration and delivery.", ["Pipelines", "Build Steps", "Artifacts", "Automation"]),
            ],
            "intermediate": [
                ("Docker", "Containerize applications for consistent deployments.", ["Images", "Containers", "Dockerfile", "Docker Compose"]),
                ("Kubernetes Basics", "Orchestrate containers at scale.", ["Pods", "Services", "Deployments", "ConfigMaps"]),
                ("Infrastructure as Code", "Manage infrastructure programmatically.", ["Terraform Basics", "Modules", "State", "Providers"]),
            ],
            "advanced": [
                ("Monitoring", "Observe systems in production.", ["Prometheus", "Grafana", "Dashboards", "SLOs"]),
                ("Security Ops", "Secure deployment pipelines and infrastructure.", ["Secrets Management", "SBOM", "Scanning", "Zero Trust"]),
                ("Platform Engineering", "Build internal developer platforms.", ["Golden Paths", "Self-Service", "Templates", "Governance"]),
            ],
        },
    },
    {
        "name": "QA Engineering",
        "slug": "qa-engineering",
        "description": "Ensure software quality through testing strategies and automation.",
        "icon": "check-circle",
        "skills_by_level": {
            "beginner": [
                ("Testing Fundamentals", "Core testing concepts and terminology.", ["Test Types", "Test Cases", "Bug Reports", "Test Plans"]),
                ("Manual Testing", "Execute structured manual test scenarios.", ["Exploratory Testing", "Regression", "Smoke Tests", "Checklists"]),
                ("Test Documentation", "Write clear, actionable test documentation.", ["Test Cases", "Traceability", "Acceptance Criteria", "Reports"]),
            ],
            "intermediate": [
                ("API Testing", "Validate REST APIs with automated tools.", ["Postman", "Status Codes", "Assertions", "Collections"]),
                ("Test Automation", "Automate UI and API tests.", ["Selenium", "Playwright", "Page Objects", "Fixtures"]),
                ("Performance Testing", "Measure system performance under load.", ["Load Tests", "Stress Tests", "Metrics", "Bottlenecks"]),
            ],
            "advanced": [
                ("Test Strategy", "Design organization-wide QA strategies.", ["Risk-Based Testing", "Shift-Left", "Quality Gates", "Metrics"]),
                ("CI Test Integration", "Integrate tests into CI/CD pipelines.", ["Parallel Runs", "Flaky Tests", "Coverage", "Reporting"]),
                ("Security Testing", "Identify vulnerabilities through testing.", ["OWASP", "Pen Testing Basics", "SAST", "DAST"]),
            ],
        },
    },
    {
        "name": "Data Analytics",
        "slug": "data-analytics",
        "description": "Analyze data to extract insights and support business decisions.",
        "icon": "bar-chart",
        "skills_by_level": {
            "beginner": [
                ("Excel & Spreadsheets", "Analyze data with spreadsheet tools.", ["Formulas", "Pivot Tables", "Charts", "Data Cleaning"]),
                ("Statistics Basics", "Foundational statistical concepts.", ["Mean & Median", "Variance", "Distributions", "Correlation"]),
                ("SQL for Analytics", "Query data for analysis.", ["Aggregations", "GROUP BY", "JOINs", "Window Functions Intro"]),
            ],
            "intermediate": [
                ("Python for Analytics", "Analyze data with pandas and numpy.", ["DataFrames", "Cleaning", "Visualization", "Aggregations"]),
                ("Data Visualization", "Communicate insights with charts.", ["Matplotlib", "Seaborn", "Dashboard Design", "Storytelling"]),
                ("Business Metrics", "Define and track KPIs.", ["KPIs", "Funnels", "Cohort Analysis", "A/B Testing Intro"]),
            ],
            "advanced": [
                ("Advanced SQL", "Complex analytical queries.", ["CTEs", "Window Functions", "Subqueries", "Optimization"]),
                ("BI Tools", "Build dashboards in BI platforms.", ["Power BI", "Looker Basics", "Semantic Models", "Self-Service BI"]),
                ("Experimentation", "Design and analyze experiments.", ["Hypothesis Testing", "Sample Size", "Significance", "Interpretation"]),
            ],
        },
    },
]

ADDITIONAL_EXPERTISE = [
    ("Data Engineering", "data-engineering", "Build data pipelines and infrastructure for analytics and ML.", "pipeline"),
    ("Machine Learning", "machine-learning", "Develop predictive models and ML-powered applications.", "brain"),
    ("Cloud Engineering", "cloud-engineering", "Design and deploy scalable cloud-native solutions.", "cloud-lightning"),
    ("Cybersecurity", "cybersecurity", "Protect systems, networks, and data from threats.", "shield"),
    ("Mobile Development", "mobile-development", "Build native and cross-platform mobile applications.", "smartphone"),
    ("System Design", "system-design", "Architect scalable, reliable distributed systems.", "network"),
]

DURATIONS = {
    "beginner": "4-6 weeks",
    "intermediate": "8-12 weeks",
    "advanced": "12-16 weeks",
}

LEVEL_TITLES = {
    "beginner": "Beginner Roadmap",
    "intermediate": "Intermediate Roadmap",
    "advanced": "Advanced Roadmap",
}


def seed():
    db = SessionLocal()
    try:
        if db.query(Expertise).first():
            print("Database already seeded. Skipping.")
            return

        if not db.query(Admin).filter(Admin.email == "admin@skillforge.ai").first():
            admin = Admin(email="admin@skillforge.ai", hashed_password=get_password_hash("admin123456"))
            db.add(admin)

        if not db.query(PromptTemplate).first():
            db.add(PromptTemplate(name="Default Skill Content", prompt_type="skill_content", template=DEFAULT_SKILL_PROMPT))
            db.add(PromptTemplate(name="Default Quiz", prompt_type="quiz", template=DEFAULT_QUIZ_PROMPT))

        for exp_data in SEED_EXPERTISE:
            expertise = Expertise(
                name=exp_data["name"],
                slug=exp_data["slug"],
                description=exp_data["description"],
                icon=exp_data["icon"],
            )
            db.add(expertise)
            db.flush()

            for level in ["beginner", "intermediate", "advanced"]:
                roadmap = Roadmap(
                    expertise_id=expertise.id,
                    title=LEVEL_TITLES[level],
                    level=RoadmapLevel(level),
                    description=f"A structured {level} path for {exp_data['name'].lower()} with hands-on skills and assessments.",
                    estimated_duration=DURATIONS[level],
                )
                db.add(roadmap)
                db.flush()

                for idx, (skill_name, skill_desc, topics) in enumerate(exp_data["skills_by_level"][level]):
                    skill = Skill(
                        roadmap_id=roadmap.id,
                        name=skill_name,
                        description=skill_desc,
                        order_index=idx,
                    )
                    db.add(skill)
                    db.flush()

                    for t_idx, topic_name in enumerate(topics):
                        topic = Topic(
                            skill_id=skill.id,
                            name=topic_name,
                            description=f"Learn the fundamentals of {topic_name.lower()} in {skill_name}.",
                            order_index=t_idx,
                        )
                        db.add(topic)

        for name, slug, description, icon in ADDITIONAL_EXPERTISE:
            expertise = Expertise(name=name, slug=slug, description=description, icon=icon)
            db.add(expertise)
            db.flush()
            for level in ["beginner", "intermediate", "advanced"]:
                roadmap = Roadmap(
                    expertise_id=expertise.id,
                    title=LEVEL_TITLES[level],
                    level=RoadmapLevel(level),
                    description=f"A structured {level} path for {name.lower()}.",
                    estimated_duration=DURATIONS[level],
                )
                db.add(roadmap)
                db.flush()
                skill = Skill(
                    roadmap_id=roadmap.id,
                    name=f"{name} Foundations",
                    description=f"Core {level} concepts for {name.lower()}.",
                    order_index=0,
                )
                db.add(skill)
                db.flush()
                for t_idx, topic_name in enumerate(["Introduction", "Core Concepts", "Practical Application", "Best Practices", "Summary"]):
                    db.add(
                        Topic(
                            skill_id=skill.id,
                            name=topic_name,
                            description=f"{topic_name} for {name}.",
                            order_index=t_idx,
                        )
                    )

        db.commit()
        print("Seed completed successfully.")
        print("Admin: admin@skillforge.ai / admin123456")
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


if __name__ == "__main__":
    seed()
