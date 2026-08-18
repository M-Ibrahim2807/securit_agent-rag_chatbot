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


