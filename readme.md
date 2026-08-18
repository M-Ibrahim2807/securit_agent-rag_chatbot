# Code Review and Security Agent

An AI-powered repository security auditing and code-assistant system built using **LangChain, ReAct Agents, FastAPI, Groq, HuggingFace Embeddings, Neon PostgreSQL, and PGVector**.

The system has two major components:

1. **ReAct-based Security Agent**
   - Dynamically selects and executes security-analysis tools.
   - Observes results.
   - Investigates findings.
   - Performs iterative reasoning and analysis.
   - Generates a security report.

2. **RAG-based Repository Assistant**
   - Indexes repository source code.
   - Stores code embeddings in PGVector.
   - Retrieves relevant code based on user questions.
   - Generates repository-grounded answers.

---

# 1. Project Structure

```text
.
├── app/
├── agent/
├── profiler/
├── security/
├── repository/
├── models/
├── prompts/
├── rag/
├── services/
├── repositories/
├── reports/
├── logs/
├── README.md
├── requirements.txt
└── .env
````

---

# 2. Application Layer

## 2.1 `app/config.py`

* Loads application configuration.
* Reads environment variables.
* Manages configuration such as:

  * Groq API key.
  * Database URL.
  * LLM model.
  * Maximum agent iterations.
  * Maximum tool calls.
  * Repository storage path.
* Provides centralized configuration to the application.

---

## 2.2 `app/database.py`

* Establishes the PostgreSQL database connection.
* Connects the application to Neon PostgreSQL.
* Configures the PGVector database.
* Provides database/session functionality to other modules.
* Handles database initialization if required.

---

## 2.3 `app/dependencies.py`

* Contains FastAPI dependency functions.
* Provides shared application components to API routes.
* Handles dependency injection for:

  * Database.
  * Repository services.
  * Agents.
  * RAG components.

---

## 2.4 `app/main.py`

* Entry point of the FastAPI application.
* Creates the FastAPI application instance.
* Registers API routes.
* Configures middleware if required.
* Starts the application through Uvicorn.

Example:

```text
FastAPI Application
        |
        +-- /audit
        |
        +-- /ask
        |
        +-- /report
```

---

## 2.5 `app/router.py`

* Defines API endpoints.
* Receives repository URLs.
* Receives repository questions.
* Calls the appropriate services.
* Returns structured API responses.

Main endpoints:

```text
POST /audit
POST /ask
GET  /report
```

---

# 3. Agent Layer

The `agent/` directory contains the **LangChain ReAct security agent**.

---

## 3.1 `agent/security_agent.py`

Main ReAct agent implementation.

Responsibilities:

* Creates the LangChain ReAct agent.
* Connects the LLM with security tools.
* Provides the repository profile to the agent.
* Provides previous observations/findings to the agent.
* Performs reasoning and tool selection.
* Decides whether additional investigation is required.
* Determines when the security audit is complete.

Core workflow:

```text
Repository Profile
        ↓
ReAct Agent
        ↓
Reason
        ↓
Select Tool
        ↓
Execute Tool
        ↓
Observe
        ↓
Analyze
        ↓
Continue / Finish
```

---

## 3.2 `agent/agent_tools.py`

Defines the tools available to the ReAct agent.

Possible tools include:

* Repository profiler.
* File reader.
* File search.
* Semgrep.
* Bandit.
* Gitleaks.
* Dependency scanner.
* Docker scanner.

Each tool is exposed to LangChain using a tool interface.

Example:

```text
@tool
run_semgrep()
```

The agent can then dynamically decide when to call it.

---

## 3.3 `agent/agent_state.py`

Maintains the state of the security investigation.

Stores information such as:

* Repository path.
* Repository profile.
* Tools already executed.
* Tool results.
* Security findings.
* Investigation history.
* Current iteration.
* Agent status.

Example:

```text
Audit State

repository
profile
observations
findings
tools_used
iteration
status
```

This allows the agent to maintain context during its investigation loop.

---

## 3.4 `agent/tool_selector.py`

Handles tool-selection logic and restrictions.

Responsibilities:

* Determines which tools are relevant to the repository.
* Prevents irrelevant tools from being used.
* Filters tools according to detected technologies.
* Applies tool execution limits.

Example:

```text
Python repository
      ↓
Bandit allowed

Java repository
      ↓
Bandit disabled
```

The ReAct agent still makes the final runtime decision, but only from an appropriate toolbox.

---

# 4. Repository Profiler

The `profiler/` directory determines what technologies and structures exist inside the repository.

The profiler is **deterministic**, not an LLM agent.

---

## 4.1 `profiler/repo_profiler.py`

Generates the repository profile.

Responsibilities:

* Analyze repository structure.
* Detect important configuration files.
* Identify package managers.
* Detect frameworks.
* Detect infrastructure files.
* Count files.
* Identify test directories.
* Identify relevant project components.

Example output:

```text
Languages:
Python
JavaScript

Frameworks:
FastAPI
React

Package Managers:
pip
npm

Docker:
Yes

Testing:
pytest
```

The resulting profile is passed to the ReAct security agent.

---

## 4.2 `profiler/language_detector.py`

Responsible for programming-language detection.

Possible implementation:

* GitHub Linguist.
* `enry`.
* File-extension analysis.

Example:

```text
.py  → Python
.js  → JavaScript
.ts  → TypeScript
.java → Java
```

The output helps determine which security tools are relevant.

---

# 5. Repository Management

The `repository/` directory manages repository acquisition and source-code access.

---

## 5.1 `repository/clone_repo.py`

Responsible for cloning repositories.

Functions include:

* Validate repository URL.
* Clone Git repository.
* Create repository workspace.
* Handle clone errors.
* Store repository locally.

Workflow:

```text
GitHub URL
    ↓
Validate
    ↓
Git Clone
    ↓
Local Repository
```

---

## 5.2 `repository/repo_manager.py`

Manages the lifecycle of the cloned repository.

Responsibilities:

* Create repository directories.
* Identify current repository.
* Clean temporary repositories.
* Track repository path.
* Manage repository metadata.

---

## 5.3 `repository/file_reader.py`

Provides controlled access to repository files.

Responsibilities:

* Read source files.
* Read specific line ranges.
* Return file content.
* Prevent access outside the repository directory.

This becomes one of the ReAct agent's tools.

---

## 5.4 `repository/file_search.py`

Searches the repository for relevant code.

Capabilities:

* Search for functions.
* Search for variables.
* Search for imports.
* Search for API endpoints.
* Search for security-sensitive functions.
* Find references to a vulnerable function.

Example:

```text
Finding:
SQL query in database.py

        ↓

File Search

        ↓

Find all usages of execute_query()
```

This helps the agent investigate findings.

---

# 6. Security Analysis Layer

The `security/` directory contains the actual security-analysis tools.

---

## 6.1 `security/semgrep_runner.py`

Runs Semgrep against the repository.

Responsibilities:

* Execute Semgrep.
* Select appropriate rules.
* Capture output.
* Parse findings.
* Return structured results.

Example:

```text
Repository
    ↓
Semgrep
    ↓
Potential vulnerabilities
```

---

## 6.2 `security/bandit_runner.py`

Runs Bandit for Python repositories.

Responsibilities:

* Execute Bandit.
* Scan Python files.
* Capture results.
* Parse Bandit output.
* Convert results into the application's finding format.

---

## 6.3 `security/gitleaks_runner.py`

Runs Gitleaks to detect exposed secrets.

Detects potential:

* API keys.
* Passwords.
* Tokens.
* Private keys.
* Credentials.

Returns structured secret findings.

---

## 6.4 `security/dependency_runner.py`

Analyzes project dependencies.

Responsibilities:

* Detect dependency files.
* Identify installed/project dependencies.
* Run the appropriate dependency scanner.
* Capture known vulnerabilities.
* Return structured dependency findings.

Examples:

```text
requirements.txt
package.json
pom.xml
```

---

## 6.5 `security/result_parser.py`

Normalizes outputs from different security tools.

This is important because each scanner produces a different output format.

For example:

```text
Semgrep JSON
Bandit JSON
Gitleaks JSON
Dependency scanner JSON
```

are converted into one common structure:

```text
Finding
├── id
├── title
├── severity
├── confidence
├── file
├── line
├── description
├── evidence
├── tool
└── status
```

This allows the ReAct agent and report generator to work with a consistent format.

---

# 7. Models

The `models/` directory contains Pydantic/data models used throughout the application.

---

## 7.1 `models/request_models.py`

Defines API request schemas.

Example:

```text
AuditRequest
    └── repository_url

AskRequest
    └── question
```

---

## 7.2 `models/response_models.py`

Defines API response schemas.

Examples:

```text
AuditResponse
AskResponse
ReportResponse
```

Provides consistent API responses.

---

## 7.3 `models/finding_models.py`

Defines the security finding structure.

Example:

```text
Finding
├── finding_id
├── title
├── severity
├── confidence
├── tool
├── file_path
├── line_number
├── description
├── evidence
├── recommendation
└── status
```

Possible statuses:

```text
Confirmed
Potential
False Positive
Informational
```

---

## 7.4 `models/repo_models.py`

Defines repository-related data structures.

Example:

```text
RepoProfile
├── languages
├── frameworks
├── dependencies
├── package_managers
├── docker
├── testing
└── repository_size
```

---

## 7.5 `models/audit_models.py`

Defines security-audit state and results.

Stores information such as:

* Audit ID.
* Repository.
* Current state.
* Tools executed.
* Findings.
* Iterations.
* Execution status.
* Final report path.

---

# 8. RAG Layer

The `rag/` directory contains the repository RAG pipeline.

This RAG is **only for repository/code understanding**.

No separate Security RAG is required.

---

## 8.1 `rag/chunker.py`

Splits repository files into chunks.

Uses:

```text
RecursiveCharacterTextSplitter
```

Responsibilities:

* Split source code.
* Configure chunk size.
* Configure chunk overlap.
* Preserve metadata such as:

  * File path.
  * Repository.
  * File type.

---

## 8.2 `rag/embedder.py`

Generates embeddings for repository chunks.

Current model:

```text
all-MiniLM-L6-v2
```

Uses:

```text
HuggingFaceEmbeddings
```

Workflow:

```text
Code Chunk
    ↓
Embedding Model
    ↓
Vector
```

---

## 8.3 `rag/vector_store.py`

Handles vector storage.

Uses:

```text
Neon PostgreSQL
+
PGVector
```

Responsibilities:

* Connect to PGVector.
* Add documents.
* Store embeddings.
* Perform similarity search.
* Retrieve metadata.

---

## 8.4 `rag/retriever.py`

Handles retrieval for the repository assistant.

Workflow:

```text
User Question
      ↓
Question Embedding
      ↓
PGVector
      ↓
Similarity Search
      ↓
Top-K Chunks
```

Returns the most relevant repository code.

---

## 8.5 `rag/indexer.py`

Coordinates repository indexing.

Workflow:

```text
Repository
     ↓
Read Files
     ↓
Chunk Files
     ↓
Generate Embeddings
     ↓
Store in PGVector
```

It acts as the main entry point for creating/updating the repository's vector index.

---

# 9. Prompts

The `prompts/` directory contains LLM prompts.

---

## 9.1 `prompts/security_agent_prompt.py`

Contains the system instructions for the ReAct security agent.

Defines:

* Agent role.
* Security-audit objectives.
* Tool usage rules.
* Investigation behavior.
* Finding verification rules.
* Maximum investigation depth.
* Safety restrictions.
* Final output requirements.

The agent should be instructed to:

```text
Do not blindly trust scanner findings.

Investigate important findings.

Use additional tools when evidence is insufficient.

Stop when sufficient evidence has been collected.

Do not modify the repository.
```

---

## 9.2 `prompts/repo_assistant_prompt.py`

Contains the prompt used by the repository RAG assistant.

Defines:

* How retrieved code should be used.
* How answers should be generated.
* How to handle missing context.
* How to reference file paths.
* How to avoid hallucinating repository information.

---

# 10. Services

The `services/` directory contains higher-level application workflows.

---

## 10.1 `services/audit_service.py`

Main security-audit orchestration service.

Workflow:

```text
Repository URL
      ↓
Clone Repository
      ↓
Profile Repository
      ↓
Create Agent
      ↓
Run ReAct Investigation
      ↓
Collect Findings
      ↓
Verify Findings
      ↓
Generate Report
      ↓
Index Repository
```

This service coordinates the components but does not itself perform the security reasoning.

---

## 10.2 `services/repository_assistant.py`

Handles repository questions.

Workflow:

```text
User Question
      ↓
Retriever
      ↓
Relevant Code
      ↓
Prompt
      ↓
Groq LLM
      ↓
Answer
```

---

## 10.3 `services/report_generator.py`

Generates the final security report.

Uses structured findings to produce:

```text
Summary
Severity distribution
Confirmed vulnerabilities
Potential vulnerabilities
False positives
Evidence
Affected files
Recommendations
Tool results
```

Output:

```text
reports/report.md
```

---

## 10.4 `services/llm.py`

Centralizes LLM configuration.

Responsibilities:

* Initialize Groq client.
* Configure selected model.
* Configure temperature.
* Provide LLM interface to:

  * ReAct agent.
  * Repository assistant.
  * Report generation if required.

---

# 11. Repository Storage

## `repositories/current_repository/`

Temporary/local working directory containing the currently analyzed repository.

Example:

```text
repositories/
└── current_repository/
    ├── app/
    ├── src/
    ├── requirements.txt
    └── README.md
```

The repository should be treated as untrusted input.

---

# 12. Reports

## `reports/report.md`

Stores generated security audit reports.

Example:

```text
reports/
└── report.md
```

The report contains:

* Repository information.
* Technology stack.
* Tools executed.
* Security findings.
* Severity.
* Confidence.
* Evidence.
* Affected files.
* Recommendations.
* Investigation results.

---

# 13. Logs

## `logs/`

Stores application and audit logs.

Possible information:

```text
Agent actions
Tool executions
Execution times
Errors
Scanner outputs
Audit status
```

Logs should not contain sensitive secrets such as API keys or passwords.

---

# 14. `requirements.txt`

Contains Python dependencies required by the project.

Main categories include:

### Backend

```text
fastapi
uvicorn
pydantic
```

### LangChain

```text
langchain
langchain-core
langchain-groq
langchain-community
```

### RAG

```text
sentence-transformers
pgvector
psycopg
```

### Database

```text
SQLAlchemy
```

Additional dependencies are added as security tools and services are integrated.

---

# 15. `.env`

Contains environment-specific configuration.

Example:

```env
DATABASE_URL=...
GROQ_API_KEY=...
```

The `.env` file must not be committed to Git.

---

# 16. Complete Security Audit Flow

The complete security workflow is:

```text
1. User submits repository URL
                ↓
2. Clone repository
                ↓
3. Profile repository
                ↓
4. Generate RepoProfile
                ↓
5. Initialize ReAct security agent
                ↓
6. Agent selects relevant security tool
                ↓
7. Execute selected tool
                ↓
8. Observe scanner output
                ↓
9. Analyze findings
                ↓
10. Read/search relevant source code
                ↓
11. Determine whether more evidence is needed
                ↓
12. If YES → select another tool/action
                ↓
13. Repeat investigation loop
                ↓
14. Correlate findings
                ↓
15. Verify findings
                ↓
16. Generate final security report
                ↓
17. Index repository into PGVector
                ↓
18. Repository becomes available to RAG assistant
```

---

# 17. Complete Repository Assistant Flow

```text
User Question
      ↓
Retriever
      ↓
Question Embedding
      ↓
PGVector Similarity Search
      ↓
Top-K Repository Chunks
      ↓
Prompt Construction
      ↓
Groq LLM
      ↓
Repository-Grounded Answer
```

---

