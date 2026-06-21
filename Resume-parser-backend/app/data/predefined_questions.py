"""
Predefined Skill-Based Medium Level Interview Questions with Answers
These questions are curated for technical interviews
Minimum 15 questions will be shown for any resume
"""

PREDEFINED_QUESTIONS = [
    # Python Questions
    {
        "id": 1,
        "skill": "Python",
        "question": "What is the difference between List and Tuple in Python? When should you use each?",
        "answer": "A List is mutable, meaning it can be modified after creation (add, remove, change elements), while a Tuple is immutable and cannot be changed after creation. Lists are defined using square brackets [] and Tuples using parentheses (). Performance-wise, Tuples are slightly faster and use less memory. Use Lists when you need to modify data frequently, and Tuples when data should remain constant (like coordinates or configuration values).",
        "difficulty": "Medium",
        "topics": ["Data Structures", "Memory Management", "Mutability"]
    },
    {
        "id": 2,
        "skill": "Python",
        "question": "What are decorators in Python and how do they work?",
        "answer": "Decorators are functions that modify the behavior of other functions or classes without changing their source code. They use the @decorator syntax and are commonly used for logging, authentication, caching, and access control. A decorator takes a function as input, adds some functionality, and returns a modified function. Example: @login_required decorator checks if user is authenticated before executing a view function.",
        "difficulty": "Medium",
        "topics": ["Functions", "Higher-Order Functions", "Metaprogramming"]
    },
    # JavaScript Questions
    {
        "id": 3,
        "skill": "JavaScript",
        "question": "What is the difference between 'var', 'let', and 'const'? Which one is preferred in modern JavaScript?",
        "answer": "'var' is function-scoped and gets hoisted, which can lead to bugs. 'let' and 'const' are block-scoped and were introduced in ES6. 'let' allows variable reassignment while 'const' doesn't (though object/array contents can still be modified). In modern JavaScript, 'const' is the default choice for variables that don't need reassignment, 'let' is used when reassignment is necessary, and 'var' should be avoided.",
        "difficulty": "Medium",
        "topics": ["ES6", "Scope", "Variable Declaration", "Hoisting"]
    },
    {
        "id": 4,
        "skill": "JavaScript",
        "question": "Explain the concept of closures in JavaScript with an example.",
        "answer": "A closure is a function that has access to variables from its outer (enclosing) function's scope, even after the outer function has returned. Closures are created every time a function is created. Example: A counter function that returns an inner function - the inner function remembers and can modify the count variable from the outer scope. Closures are used for data privacy, function factories, and maintaining state.",
        "difficulty": "Medium",
        "topics": ["Closures", "Scope", "Lexical Environment"]
    },
    # React Questions
    {
        "id": 5,
        "skill": "React",
        "question": "What is the purpose of useEffect hook in React? How does the dependency array work?",
        "answer": "The useEffect hook handles side effects like API calls, subscriptions, and DOM manipulation. The dependency array [] contains variables that trigger the effect to re-run when changed. An empty array [] means the effect runs only on mount. No array means it runs on every render. You can return a cleanup function for unsubscribing or cleanup. Proper dependency management prevents infinite loops and memory leaks.",
        "difficulty": "Medium",
        "topics": ["React Hooks", "Side Effects", "Component Lifecycle"]
    },
    {
        "id": 6,
        "skill": "React",
        "question": "What is the difference between useState and useReducer? When would you use each?",
        "answer": "useState is for simple state management with single values or simple objects. useReducer is better for complex state logic with multiple sub-values or when next state depends on previous state. useReducer uses a reducer function with dispatch actions, similar to Redux pattern. Use useState for form inputs, toggles, counters. Use useReducer for complex forms, state machines, or when multiple state updates happen together.",
        "difficulty": "Medium",
        "topics": ["State Management", "React Hooks", "Reducers"]
    },
    # Node.js Questions
    {
        "id": 7,
        "skill": "Node.js",
        "question": "How does the Event Loop work in Node.js? How does it handle concurrent operations while being single-threaded?",
        "answer": "Node.js works on an event-driven, non-blocking I/O model. The event loop is a continuous cycle that monitors the callback queue. When an async operation (file read, HTTP request) occurs, it goes to the background and the main thread stays free. Once completed, the callback goes to the queue and the event loop executes it. This allows handling thousands of concurrent connections efficiently despite being single-threaded.",
        "difficulty": "Medium",
        "topics": ["Asynchronous Programming", "Concurrency", "Event-Driven Architecture"]
    },
    {
        "id": 8,
        "skill": "Node.js",
        "question": "What is middleware in Express.js and how does it work?",
        "answer": "Middleware functions are functions that have access to request object (req), response object (res), and the next middleware function (next). They can execute code, modify req/res objects, end the request-response cycle, or call next middleware. Middleware is used for logging, authentication, parsing request body, error handling, and CORS. They execute in order they are defined using app.use() or route-specific methods.",
        "difficulty": "Medium",
        "topics": ["Express.js", "Request Pipeline", "Authentication"]
    },
    # SQL Questions
    {
        "id": 9,
        "skill": "SQL",
        "question": "What is the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN in SQL? Explain with examples.",
        "answer": "INNER JOIN returns only matching records from both tables - if no match exists, the row is excluded. LEFT JOIN returns all records from the left table and matching records from the right table; NULL is returned for non-matches. RIGHT JOIN is the opposite - complete right table with matching left. Example: With Students and Courses tables - INNER JOIN shows enrolled students' courses, LEFT JOIN shows all students including those without courses.",
        "difficulty": "Medium",
        "topics": ["Database", "Joins", "Query Optimization"]
    },
    {
        "id": 10,
        "skill": "SQL",
        "question": "What is the difference between WHERE and HAVING clauses in SQL?",
        "answer": "WHERE filters rows before grouping and cannot use aggregate functions. HAVING filters groups after GROUP BY and can use aggregate functions like COUNT, SUM, AVG. Example: WHERE salary > 50000 filters individual rows, HAVING COUNT(*) > 5 filters groups with more than 5 members. Use WHERE for row-level filtering on regular columns, HAVING for filtering aggregated results after grouping.",
        "difficulty": "Medium",
        "topics": ["Aggregation", "Filtering", "GROUP BY"]
    },
    # API Design Questions
    {
        "id": 11,
        "skill": "API Design",
        "question": "What is the correct usage of HTTP methods (GET, POST, PUT, DELETE) in REST API? What is Idempotency?",
        "answer": "GET is for retrieving data (safe, idempotent), POST for creating new resources (not idempotent), PUT for completely updating/replacing resources (idempotent), DELETE for removing resources (idempotent), PATCH for partial updates. Idempotency means sending the same request multiple times produces the same result. GET, PUT, DELETE are idempotent - deleting 10 times still deletes once. POST is not idempotent - 10 POST requests can create 10 resources.",
        "difficulty": "Medium",
        "topics": ["REST", "HTTP Methods", "API Best Practices"]
    },
    {
        "id": 12,
        "skill": "API Design",
        "question": "How do you handle API versioning? What are the different approaches?",
        "answer": "API versioning ensures backward compatibility when making breaking changes. Common approaches: 1) URL versioning (/api/v1/users) - most common and explicit, 2) Header versioning (Accept: application/vnd.api+json;version=1), 3) Query parameter (?version=1). Best practices: Never break existing contracts, deprecate old versions gradually, document changes clearly. URL versioning is recommended for its simplicity and discoverability.",
        "difficulty": "Medium",
        "topics": ["Versioning", "Backward Compatibility", "REST Best Practices"]
    },
    # Git Questions
    {
        "id": 13,
        "skill": "Git",
        "question": "What is the difference between 'git rebase' and 'git merge'? When should you use each?",
        "answer": "Merge combines two branches by creating a merge commit and preserves complete history. Rebase moves commits from the current branch to the top of the target branch, creating a linear history. Merge is safer and better for team collaboration. Rebase provides cleaner history but is risky on shared branches as it changes commit hashes. Rule: Use merge on public/shared branches, use rebase on private/local branches.",
        "difficulty": "Medium",
        "topics": ["Version Control", "Branching Strategy", "Collaboration"]
    },
    {
        "id": 14,
        "skill": "Git",
        "question": "What is git stash and when would you use it?",
        "answer": "Git stash temporarily saves uncommitted changes (both staged and unstaged) so you can work on something else. Use 'git stash' to save, 'git stash pop' to restore and remove from stash, 'git stash apply' to restore but keep in stash. Use cases: switching branches without committing incomplete work, pulling latest changes when you have local modifications, quickly testing something on clean state.",
        "difficulty": "Medium",
        "topics": ["Version Control", "Workflow", "Temporary Storage"]
    },
    # Data Structures Questions
    {
        "id": 15,
        "skill": "Data Structures",
        "question": "What is collision in HashMap/Dictionary and how is it handled?",
        "answer": "Collision occurs when two different keys produce the same hash value and try to go into the same bucket. There are two main handling methods: 1) Chaining - storing in a linked list/tree within the same bucket, 2) Open Addressing - finding the next available slot (linear probing, quadratic probing, double hashing). Collisions are minimized with a good hash function and maintaining proper load factor (typically 0.75). Java HashMap uses chaining with tree-ification.",
        "difficulty": "Medium",
        "topics": ["Hash Tables", "Collision Resolution", "Time Complexity"]
    },
    {
        "id": 16,
        "skill": "Data Structures",
        "question": "What is the difference between Stack and Queue? Give real-world examples of each.",
        "answer": "Stack follows LIFO (Last In First Out) - last element added is first removed. Queue follows FIFO (First In First Out) - first element added is first removed. Stack examples: browser back button, undo functionality, function call stack. Queue examples: print job queue, message queues, BFS algorithm. Stack operations are push/pop, Queue operations are enqueue/dequeue. Both have O(1) time complexity for basic operations.",
        "difficulty": "Medium",
        "topics": ["Linear Data Structures", "LIFO", "FIFO"]
    },
    # Angular Questions
    {
        "id": 17,
        "skill": "Angular",
        "question": "What are the Component lifecycle hooks in Angular? What is the difference between ngOnInit and constructor?",
        "answer": "Angular's main lifecycle hooks are: ngOnChanges (input changes), ngOnInit (component initialization), ngDoCheck (change detection), ngAfterContentInit/Checked (content projection), ngAfterViewInit/Checked (view rendering), ngOnDestroy (cleanup). Constructor is a TypeScript/JavaScript feature used for dependency injection. ngOnInit is an Angular hook called after component is fully initialized when inputs are available. Keep heavy initialization logic in ngOnInit, constructor is only for DI.",
        "difficulty": "Medium",
        "topics": ["Component Lifecycle", "Dependency Injection", "Angular Framework"]
    },
    {
        "id": 18,
        "skill": "Angular",
        "question": "What are Observables in Angular and how do they differ from Promises?",
        "answer": "Observables (from RxJS) are lazy, can emit multiple values over time, and are cancellable. Promises are eager, emit single value, and cannot be cancelled. Observables support operators like map, filter, debounce for stream manipulation. Use subscribe() to consume Observables. In Angular, HTTP client returns Observables. Use Promises for single async operations, Observables for streams of data, event handling, and when you need cancellation or operators.",
        "difficulty": "Medium",
        "topics": ["RxJS", "Async Programming", "Streams"]
    },
    # Database Questions
    {
        "id": 19,
        "skill": "Database",
        "question": "What is Database Indexing? What are its advantages and disadvantages?",
        "answer": "An Index is a data structure that speeds up database queries by maintaining pointers to rows, like a book's index helps find specific topics quickly. Advantages: SELECT queries become much faster, WHERE, ORDER BY, JOIN operations are optimized. Disadvantages: Extra storage space is required, INSERT/UPDATE/DELETE become slower as indexes also need updating. Best practice: Index frequently searched columns, more indexes are fine on rarely updated tables.",
        "difficulty": "Medium",
        "topics": ["Database Optimization", "Query Performance", "B-Tree"]
    },
    {
        "id": 20,
        "skill": "Database",
        "question": "What is the difference between SQL and NoSQL databases? When would you choose each?",
        "answer": "SQL databases are relational, use structured schemas with tables, support ACID transactions, and use SQL language (MySQL, PostgreSQL). NoSQL databases are non-relational, schema-flexible, horizontally scalable, and include document, key-value, graph types (MongoDB, Redis). Choose SQL for complex queries, transactions, structured data. Choose NoSQL for large scale, flexible schema, high write loads, real-time applications, and when horizontal scaling is priority.",
        "difficulty": "Medium",
        "topics": ["SQL vs NoSQL", "Database Selection", "Scalability"]
    },
    # Security Questions
    {
        "id": 21,
        "skill": "Security",
        "question": "What is SQL Injection and how can it be prevented?",
        "answer": "SQL Injection is a security vulnerability where attackers inject malicious SQL code through user input. Example: entering 'admin'--' in username field to bypass password check. Prevention methods: 1) Use Parameterized Queries/Prepared Statements (most effective), 2) Input validation and sanitization, 3) Use ORMs that provide automatic escaping, 4) Least privilege principle - give database user limited permissions, 5) Web Application Firewall. Never dynamically concatenate user input into SQL queries.",
        "difficulty": "Medium",
        "topics": ["Web Security", "OWASP", "Input Validation"]
    },
    {
        "id": 22,
        "skill": "Security",
        "question": "What is JWT (JSON Web Token) and how does it work for authentication?",
        "answer": "JWT is a compact, URL-safe token format for securely transmitting information between parties. It has three parts: Header (algorithm, type), Payload (claims/data), Signature (verification). User logs in, server creates JWT with user data and secret, client stores token and sends with requests, server verifies signature. Benefits: Stateless (no session storage), scalable, works across domains. Risks: Token theft, no revocation without extra logic.",
        "difficulty": "Medium",
        "topics": ["Authentication", "Token-Based Auth", "Stateless"]
    },
    # System Design Questions
    {
        "id": 23,
        "skill": "System Design",
        "question": "What is the difference between Horizontal Scaling and Vertical Scaling? When is each approach better?",
        "answer": "Vertical Scaling (Scale Up) makes the existing server more powerful by adding more RAM, CPU, and storage. Horizontal Scaling (Scale Out) adds multiple servers and distributes load. Vertical: Simple implementation, no code changes needed, but has hardware limits and single point of failure. Horizontal: Theoretically unlimited scaling, better fault tolerance, but requires complex architecture, load balancer, and data consistency is challenging. Modern applications prefer horizontal scaling as cloud servers can be easily added/removed.",
        "difficulty": "Medium",
        "topics": ["Scalability", "Load Balancing", "Cloud Architecture"]
    },
    {
        "id": 24,
        "skill": "System Design",
        "question": "What is a Load Balancer and what algorithms does it use?",
        "answer": "A Load Balancer distributes incoming network traffic across multiple servers to ensure reliability and performance. Common algorithms: Round Robin (sequential distribution), Weighted Round Robin (based on server capacity), Least Connections (to server with fewest active connections), IP Hash (consistent routing based on client IP). Load balancers also perform health checks, SSL termination, and session persistence. Examples: AWS ELB, Nginx, HAProxy.",
        "difficulty": "Medium",
        "topics": ["Traffic Distribution", "High Availability", "Algorithms"]
    },
    # Cloud & DevOps Questions
    {
        "id": 25,
        "skill": "Cloud",
        "question": "What is Docker and why is containerization important?",
        "answer": "Docker is a platform for developing, shipping, and running applications in containers. Containers package application code with dependencies, ensuring consistent behavior across environments. Benefits: Faster deployments, resource efficiency (lighter than VMs), isolation, portability, scalability. Key concepts: Dockerfile (build instructions), Images (templates), Containers (running instances), Docker Compose (multi-container apps). Containerization solves 'works on my machine' problem.",
        "difficulty": "Medium",
        "topics": ["Containerization", "DevOps", "Microservices"]
    },
    {
        "id": 26,
        "skill": "Cloud",
        "question": "What is CI/CD and why is it important in modern software development?",
        "answer": "CI (Continuous Integration) automatically builds and tests code when developers push changes. CD (Continuous Deployment/Delivery) automatically deploys tested code to production. Benefits: Faster release cycles, early bug detection, reduced manual errors, consistent deployments, quick rollbacks. Pipeline stages: Code commit → Build → Test → Deploy to staging → Deploy to production. Tools: Jenkins, GitHub Actions, GitLab CI, CircleCI.",
        "difficulty": "Medium",
        "topics": ["Automation", "DevOps", "Deployment Pipeline"]
    },
    # Testing Questions
    {
        "id": 27,
        "skill": "Testing",
        "question": "What is the difference between Unit Testing, Integration Testing, and E2E Testing?",
        "answer": "Unit Testing tests individual functions/components in isolation with mocked dependencies - fast, many tests. Integration Testing tests how multiple units work together, including real databases/APIs - slower, fewer tests. E2E (End-to-End) Testing tests complete user flows through the actual application - slowest, fewest tests. Testing pyramid suggests: Many unit tests (base), fewer integration tests (middle), fewest E2E tests (top). Each level catches different types of bugs.",
        "difficulty": "Medium",
        "topics": ["Testing Pyramid", "Quality Assurance", "Test Automation"]
    },
    {
        "id": 28,
        "skill": "Testing",
        "question": "What is Test-Driven Development (TDD) and what are its benefits?",
        "answer": "TDD is a development approach where you write tests before writing the actual code. Cycle: Red (write failing test) → Green (write minimal code to pass) → Refactor (improve code while keeping tests passing). Benefits: Better code design, documentation through tests, confidence in refactoring, fewer bugs, forces thinking about requirements first. Challenges: Slower initial development, learning curve, maintaining test suite. Works best with unit tests.",
        "difficulty": "Medium",
        "topics": ["Testing Methodology", "Code Quality", "Development Process"]
    },
    # General Programming Questions
    {
        "id": 29,
        "skill": "Programming",
        "question": "What is the difference between synchronous and asynchronous programming?",
        "answer": "Synchronous programming executes code line by line, blocking until each operation completes. Asynchronous programming allows operations to run in background without blocking, using callbacks, promises, or async/await. Sync is simpler but can freeze UI/block thread. Async is complex but essential for I/O operations, API calls, file operations. Example: Sync file read blocks until complete; Async file read returns immediately and notifies when done.",
        "difficulty": "Medium",
        "topics": ["Concurrency", "Non-blocking", "Performance"]
    },
    {
        "id": 30,
        "skill": "Programming",
        "question": "What are SOLID principles in object-oriented programming?",
        "answer": "SOLID is five design principles for maintainable code: S - Single Responsibility (one class, one job), O - Open/Closed (open for extension, closed for modification), L - Liskov Substitution (subclasses should be substitutable for parent), I - Interface Segregation (many specific interfaces better than one general), D - Dependency Inversion (depend on abstractions, not concretions). Following SOLID leads to flexible, testable, maintainable code.",
        "difficulty": "Medium",
        "topics": ["OOP", "Design Principles", "Clean Code"]
    }
]


# Skill mapping for better matching
SKILL_MAPPING = {
    "python": ["python", "py", "django", "flask", "fastapi", "pandas", "numpy", "pytorch", "tensorflow"],
    "javascript": ["javascript", "js", "typescript", "ts", "es6", "ecmascript", "jquery"],
    "react": ["react", "reactjs", "react.js", "redux", "next.js", "nextjs", "gatsby"],
    "node.js": ["node", "nodejs", "node.js", "express", "expressjs", "npm", "nestjs", "koa"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle", "mssql", "sql server", "mariadb"],
    "api design": ["api", "rest", "restful", "graphql", "swagger", "openapi", "postman", "grpc"],
    "git": ["git", "github", "gitlab", "bitbucket", "version control", "svn"],
    "data structures": ["data structures", "algorithms", "dsa", "leetcode", "array", "linked list", "tree", "graph", "sorting"],
    "angular": ["angular", "angularjs", "angular.js", "rxjs", "ngrx"],
    "database": ["database", "mongodb", "redis", "cassandra", "dynamodb", "nosql", "db", "firebase", "supabase"],
    "security": ["security", "cybersecurity", "authentication", "authorization", "oauth", "jwt", "encryption", "ssl", "https"],
    "system design": ["system design", "architecture", "microservices", "distributed systems", "scalability", "load balancing", "caching"],
    "cloud": ["cloud", "aws", "azure", "gcp", "docker", "kubernetes", "k8s", "terraform", "devops", "ci/cd", "jenkins"],
    "testing": ["testing", "jest", "mocha", "pytest", "junit", "cypress", "selenium", "tdd", "bdd", "unit test"],
    "programming": ["programming", "coding", "software", "development", "engineering", "oop", "functional"]
}


def get_predefined_questions():
    """Return all predefined questions"""
    return PREDEFINED_QUESTIONS


def get_questions_by_skill(skill: str):
    """Return questions filtered by skill"""
    skill_lower = skill.lower()
    return [q for q in PREDEFINED_QUESTIONS if skill_lower in q["skill"].lower()]


def get_questions_for_resume_skills(user_skills: list, min_questions: int = 15):
    """
    Match user's resume skills with predefined questions
    Returns at least min_questions questions
    First matched questions, then fill with remaining to reach minimum
    """
    if not user_skills:
        return PREDEFINED_QUESTIONS[:min_questions]
    
    matched_questions = []
    matched_question_ids = set()
    
    # Normalize user skills
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    
    for question in PREDEFINED_QUESTIONS:
        question_skill = question["skill"].lower()
        
        # Check direct match
        for user_skill in user_skills_lower:
            # Direct match
            if question_skill in user_skill or user_skill in question_skill:
                if question["id"] not in matched_question_ids:
                    matched_questions.append(question)
                    matched_question_ids.add(question["id"])
                break
            
            # Check through skill mapping
            for mapped_skill, keywords in SKILL_MAPPING.items():
                if mapped_skill == question_skill:
                    for keyword in keywords:
                        if keyword in user_skill or user_skill in keyword:
                            if question["id"] not in matched_question_ids:
                                matched_questions.append(question)
                                matched_question_ids.add(question["id"])
                            break
    
    # If matched questions are less than minimum, add more from remaining
    if len(matched_questions) < min_questions:
        remaining_questions = [q for q in PREDEFINED_QUESTIONS if q["id"] not in matched_question_ids]
        questions_needed = min_questions - len(matched_questions)
        matched_questions.extend(remaining_questions[:questions_needed])
    
    # Renumber questions for user
    result = []
    for idx, q in enumerate(matched_questions, 1):
        q_copy = q.copy()
        q_copy["id"] = idx
        result.append(q_copy)
    
    return result
