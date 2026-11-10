# Text-to-SQL AI with Clarification Engine

An AI-powered Text-to-SQL application that allows users to query a relational database using natural language.

The system converts natural-language questions into SQL, detects ambiguous questions, asks clarification questions, validates generated SQL for safety, executes read-only queries, and converts database results into natural-language answers.

---

##  Features

-  Natural-language database querying
-  LLM-powered Text-to-SQL generation
-  Clarification engine for ambiguous questions
-  Database schema-aware SQL generation
-  Read-only SQL validation
-  Destructive-intent detection
-  SQLite database execution
-  Structured database results
-  Natural-language response generation
-  FastAPI backend
-  Browser-based chat interface
-  Automated security tests

---

##  Architecture

```text
User
 │
 ▼
Web Interface
 │
 ▼
FastAPI API
 │
 ▼
Clarification Engine
 │
 ├── Ambiguous ──► Ask Follow-up
 │
 ▼
LLM
 │
 ▼
SQL Generator
 │
 ▼
SQL Safety Checks
 │
 ├── Dangerous ──► Block
 │
 ▼
SQLite Database
 │
 ▼
Result Formatter
 │
 ▼
Natural-language Answer


## Tech Stack
Python
FastAPI
Groq API
SQLite
HTML
CSS
JavaScript
Pytest