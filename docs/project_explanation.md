# SQL Analyst Agent - Project Explanation

This document provides detailed explanations of the technologies and components used in this project.

---

## 🎯 Project Overview

This is an **intelligent SQL database query agent** that allows users to ask questions in natural language and automatically generates SQL queries to retrieve answers from a MySQL database. The key innovation is **extreme token efficiency** - using 98.5% fewer tokens than traditional chatbot approaches.

---

## 📁 Folder Structure Explained

Understanding the project layout is crucial. Let me explain why each folder exists and why certain files are in the root directory.

### **Root Directory Files** (6 files)

These files are in the root because they need to be **easily accessible and executable** by you and the operating system:

#### 1. `.env` - Environment Variables (Secret Storage)
**Purpose:** Stores sensitive information like API keys
- **Why in root:** Python's `python-dotenv` library automatically looks for `.env` in the project root
- **Contents:** `GROQ_API_KEY=your_key_here`
- **Security:** Never commit this to GitHub! (It's in `.gitignore`)
- **Used by:** Both `main.py` and `app.py` to authenticate with Groq API

#### 2. `config.yaml` - Configuration File
**Purpose:** All project settings in one readable file
- **Why in root:** Central location where both CLI and web server can easily find it
- **Contents:** 
  - Groq model settings (which model, max tokens, temperature)
  - Database connection details (host, user, password, database name)
  - Cache settings (how long to cache, when to clear)
  - Token budget limits
- **Used by:** Both `main.py` and `app.py` read this on startup
- **Benefit:** Change settings without touching code!

#### 3. `main.py` - Command Line Interface Entry Point
**Purpose:** Launches the CLI version of the agent (terminal-based)
- **Why in root:** Makes it easy to run: `python main.py`
- **What it does:**
  - Loads configuration from `config.yaml` and `.env`
  - Initializes the agent (Groq client, database tools, cache)
  - Starts an interactive terminal session
  - Lets you ask questions in the terminal
- **When to use:** Quick testing, development, or if you prefer terminal over web UI

#### 4. `app.py` - Web Server Entry Point
**Purpose:** Launches the FastAPI web server (web-based UI)
- **Why in root:** Makes it easy to run: `python app.py`
- **What it does:**
  - Creates a REST API with endpoints (`/api/ask`, `/api/stats`, etc.)
  - Serves the web interface from `web/index.html`
  - Handles multiple users simultaneously
  - Provides a beautiful web UI for asking questions
- **When to use:** Production use, when you want a nice UI, or when sharing with others

#### 5. `requirements.txt` - Python Dependencies
**Purpose:** Lists all Python packages your project needs
- **Why in root:** Standard Python convention - all projects have this in root
- **Contents:** Package names and versions (langgraph, fastapi, groq, etc.)
- **Used by:** `pip install -r requirements.txt` to install all dependencies
- **Benefit:** Anyone can set up your project with one command!

#### 6. `README.md` - Main Documentation
**Purpose:** The "front door" of your project - first thing people see
- **Why in root:** GitHub automatically displays this on your repository homepage
- **Contents:**
  - Quick start guide
  - Usage examples
  - Installation instructions
  - Project overview
- **Audience:** New users, collaborators, or your future self!

---

### **`src/` Folder** - Source Code (The Brain 🧠)

This is where **all the core logic** lives. It's organized into modules by functionality:

#### `src/agent/` - LangGraph Workflow
**Purpose:** The orchestration layer - controls the multi-step workflow
- **Files:**
  - `state.py` - Defines what data flows between steps (question, SQL, results, tokens, etc.)
  - `nodes.py` - Each node is one step in the workflow (parse question → generate SQL → execute → format answer)
  - `graph.py` - Connects all the nodes together into a complete workflow
- **Why separate folder:** Agent logic is complex and deserves its own module
- **Analogy:** Think of this as the "conductor" of an orchestra - coordinates everyone

#### `src/mcp/` - Database Tools
**Purpose:** All database interaction happens here (MCP = Model Context Protocol)
- **Files:**
  - `tools.py` - Functions to query database (get tables, get schema, execute SQL, etc.)
- **Why separate folder:** Keeps database logic isolated from AI logic
- **Benefit:** Want to switch to PostgreSQL? Just modify this folder!
- **Analogy:** This is your "toolbox" - the agent asks these tools to do database work

#### `src/llm/` - Large Language Model Integration
**Purpose:** All LLM-related code (talking to Groq API)
- **Files:**
  - `groq_client.py` - Handles API calls to Groq, tracks token usage
  - `prompts.py` - Carefully crafted prompts to minimize tokens and maximize accuracy
- **Why separate folder:** LLM logic should be independent from workflow logic
- **Benefit:** Want to switch to OpenAI? Just modify this folder!
- **Analogy:** This is your "translator" - converts natural language ↔ SQL

#### `src/cache/` - Schema Caching System
**Purpose:** Remembers database schemas to save tokens
- **Files:**
  - `schema_cache.py` - Stores table schemas in memory for 30 minutes
- **Why separate folder:** Caching is a distinct responsibility
- **Benefit:** First query fetches schema (~200 tokens), next 19 queries reuse it (0 tokens!)
- **Analogy:** This is your "memory" - remembers things so you don't have to ask twice

#### `src/ui/` - User Interface (CLI)
**Purpose:** Terminal-based user interface code
- **Files:**
  - `cli.py` - Handles user input, displays results, shows token stats in terminal
- **Why separate folder:** UI code should be separate from business logic
- **Benefit:** Could add a GUI later without touching the core agent!

---

### **`web/` Folder** - Web Interface (The Face 👤)

**Purpose:** Contains the web-based user interface
- **Files:**
  - `index.html` - The beautiful web UI (HTML/CSS/JavaScript)
- **Why separate folder:** 
  - Keeps frontend code separate from backend Python code
  - Easy to find and modify the web UI
  - Could expand to multiple HTML files later
- **Served by:** `app.py` (FastAPI serves this file)
- **Access:** When you run `python app.py` and visit `http://localhost:8000`

---

### **`docs/` Folder** - Documentation (The Library 📚)

**Purpose:** All documentation files organized in one place
- **Files:**
  - `setup.md` - Step-by-step setup instructions
  - `quick_reference.md` - Quick command reference
  - `web_interface_guide.md` - How to use the web UI
  - `project_explanation.md` - This file! (Technology breakdown)
- **Why separate folder:**
  - Keeps root directory clean
  - Easy to find all documentation
  - Professional project organization
- **When to use:** When you need help, want to understand something, or onboard new users

---

### **`scripts/` Folder** - Utility Scripts (The Toolkit 🔧)

**Purpose:** Helper scripts that don't run regularly
- **Files:**
  - `setup_db.py` - One-time script to create and populate MySQL database
  - `start_web.ps1` - PowerShell script to quickly start the web server
- **Why separate folder:**
  - These aren't part of the core application
  - Used occasionally for setup/maintenance
  - Keeps root directory focused on main entry points
- **When to use:** During setup or when you need to reset the database

---

### **`sql_analyst/` Folder** - Virtual Environment (Hidden)

**Purpose:** Isolated Python environment with all dependencies
- **Contents:** Python interpreter + installed packages (FastAPI, LangGraph, etc.)
- **Why it exists:** 
  - Prevents conflicts with other Python projects
  - Each project gets its own package versions
- **Why you don't see it much:** It's automatically used when activated
- **Activate with:** `.\sql_analyst\Scripts\activate` (on Windows)

---

## 🎨 Design Philosophy: Why This Structure?

### **Separation of Concerns**
- Each folder has **one clear purpose**
- Easy to find what you're looking for
- Example: All database code in `src/mcp/`, all LLM code in `src/llm/`

### **Scalability**
- Want to add more database tools? → Add to `src/mcp/`
- Want to add more prompts? → Add to `src/llm/prompts.py`
- Want more documentation? → Add to `docs/`

### **Professional Standards**
- Follows **Python best practices**
- Similar to how big companies organize code
- Easy for other developers to understand

### **Ease of Use**
- Entry points (`main.py`, `app.py`) in root = easy to run
- Config files (`.env`, `config.yaml`) in root = easy to modify
- Documentation in `docs/` = easy to find help

---

## 📊 Folder Hierarchy Visual

```
d:/sql_analyst/
│
├─── 🏠 ROOT (6 files)
│    ├─ .env              → Secrets (API keys)
│    ├─ config.yaml       → Settings (model, DB, cache)
│    ├─ main.py          → Run CLI version
│    ├─ app.py           → Run web server
│    ├─ requirements.txt → Install dependencies
│    └─ README.md        → Start here!
│
├─── 🧠 src/ (The Brain - Core Logic)
│    ├─ agent/           → Workflow orchestration (LangGraph)
│    ├─ mcp/             → Database tools
│    ├─ llm/             → LLM integration (Groq)
│    ├─ cache/           → Token-saving cache
│    └─ ui/              → Terminal UI
│
├─── 👤 web/ (The Face - User Interface)
│    └─ index.html       → Beautiful web UI
│
├─── 📚 docs/ (The Library - Documentation)
│    ├─ setup.md
│    ├─ quick_reference.md
│    ├─ web_interface_guide.md
│    └─ project_explanation.md (this file!)
│
├─── 🔧 scripts/ (The Toolkit - Utilities)
│    ├─ setup_db.py      → Create database
│    └─ start_web.ps1    → Quick launcher
│
└─── 📦 sql_analyst/ (Virtual Environment - Hidden)
     └─ Scripts/, Lib/, etc.
```

---

## 🔑 Key Takeaways

### Root Files = **Action & Configuration**
- If you want to **run** something → Look in root (`main.py`, `app.py`)
- If you want to **configure** something → Look in root (`.env`, `config.yaml`)

### `src/` Folder = **The Engine**
- All the intelligence lives here
- Modify this when adding features

### `web/` Folder = **The Interface**
- What users see and interact with
- Modify this for UI changes

### `docs/` Folder = **The Manual**
- Learn how things work
- Help for setup and usage

### `scripts/` Folder = **The Toolbox**
- One-time setup or maintenance tasks

---


## 🛠️ Technologies Used

### 1. **LangGraph**

**What it is:**
- A framework developed by LangChain for building **stateful, multi-step AI workflows**
- Think of it as a state machine that orchestrates different steps in a workflow

**Why we use it:**
- Our agent needs to perform **multiple sequential steps**:
  1. Understand the question
  2. Generate SQL query
  3. Execute the query
  4. Format the results
  5. Handle errors and retry if needed
- LangGraph manages this workflow, ensuring each step has access to the right data
- Provides built-in **state management** so the agent remembers context between steps
- Makes it easy to add **retry logic** and **error handling**

**How it's used in our project:**
- Defined in `src/agent/graph.py`
- Creates a workflow with nodes (steps) and edges (transitions between steps)
- Each node performs a specific task (e.g., "generate SQL", "execute query")

---

### 2. **Groq API (LLM Provider)**

**What it is:**
- A **cloud-based LLM service** that provides ultra-fast inference
- Similar to OpenAI, but optimized for speed using custom hardware (LPU)
- We use their `llama-3.3-70b-versatile` model

**Why we use it:**
- **Free tier** with generous token limits (~6,000 tokens/minute)
- **Extremely fast** responses (sub-second generation)
- **Cost-effective** for token-conscious applications
- Supports the **Llama 3.3** model which is excellent at code generation

**How it's used in our project:**
- Client implementation in `src/llm/groq_client.py`
- Used to:
  - Convert natural language questions into SQL queries
  - Format query results into human-readable answers
- Tracks token usage for each API call to stay within budget

---

### 3. **MCP-Style Database Tools (Custom Built)**

**What it is:**
- **MCP** = Model Context Protocol (a pattern for tool-use)
- **Our implementation:** Custom Python class we built from scratch
- Think of it as a "toolbox" for database operations
- **NOT an official MCP server** - we built our own tools following the MCP philosophy!

**Why we use this pattern:**
- Separates **database logic** from **AI logic**
- The LLM doesn't execute SQL directly - it asks our tools to do it
- Provides safety and control over database operations
- Makes it easy to switch databases (MySQL → PostgreSQL) without changing agent logic

**How it's used in our project:**
- Implemented in `src/mcp/tools.py` (we wrote this ourselves!)
- Provides functions like:
  - `list_tables()` - List all tables
  - `get_table_schema(table)` - Get structure of a table
  - `execute_query(query)` - Run a SQL query
  - `get_sample_data(table)` - Get example rows
  - `get_table_count(table)` - Count rows in a table
- Uses `mysql-connector-python` library for direct MySQL connections
- The agent calls these tools instead of accessing the database directly

**Important Clarification:**
There ARE official MCP servers (like `@modelcontextprotocol/server-sqlite` or `@modelcontextprotocol/server-postgres`), but we're NOT using them. We built our own custom tools because:
- **More control** - We can optimize exactly for our use case
- **Simpler** - No need to set up external MCP server infrastructure
- **Direct integration** - Python class directly in our codebase
- **No dependencies** - Just standard MySQL connector

Our `DatabaseTools` class is a **custom implementation** inspired by the MCP philosophy, not a pre-built MCP server!

---

### 4. **MySQL Database**

**What it is:**
- A popular **relational database management system (RDBMS)**
- Stores structured data in tables with rows and columns

**Why we use it:**
- **Free and open-source**
- **Industry standard** for web applications
- **Fast performance** for analytical queries
- Easy to set up locally for development

**How it's used in our project:**
- Stores the `retail_analytics` database with:
  - `customers` table (1,000 rows)
  - `products` table (200 rows)
  - `orders` table (10,000 rows)
- Connected via `mysql-connector-python` library
- Configuration in `config.yaml`

---

### 5. **FastAPI (Web Framework)**

**What it is:**
- A modern **Python web framework** for building APIs
- Fast, easy to use, with automatic API documentation

**Why we use it:**
- Provides a **REST API** so users can query the agent from a web interface
- **Asynchronous support** for handling multiple requests
- **Type validation** with Pydantic models
- Built-in **Swagger UI** for testing API endpoints

**How it's used in our project:**
- Main server file: `app.py`
- Provides endpoints:
  - `POST /api/ask` - Ask a question
  - `GET /api/stats` - Get token usage stats
  - `GET /api/reset` - Reset session
- Serves the web interface HTML from `web/index.html`

---

### 6. **Schema Caching System**

**What it is:**
- A **custom-built cache** that stores database schema information
- Implemented in `src/cache/schema_cache.py`

**Why we use it:**
- **Token savings**: Database schemas don't change often, so we cache them
- The first time a table is queried, we fetch and cache its schema
- Subsequent queries reuse the cached schema (0 tokens!)
- This alone saves ~100-200 tokens per question

**How it's used in our project:**
- Stores:
  - Table names
  - Column names and types
  - Relationships between tables
- Auto-expires after 30 minutes
- Clears after 20 questions to ensure freshness

---

### 7. **Python-dotenv**

**What it is:**
- A library that loads environment variables from a `.env` file

**Why we use it:**
- **Security**: Keeps API keys out of source code
- **Convenience**: One central place for configuration
- Prevents accidental commit of secrets to GitHub

**How it's used in our project:**
- Loads `GROQ_API_KEY` from `.env` file
- Used in `app.py` and `main.py`

---

### 8. **PyYAML**

**What it is:**
- A library for parsing YAML configuration files

**Why we use it:**
- **Human-readable config**: YAML is easier to read than JSON
- **Centralized settings**: All configuration in one `config.yaml` file
- Easy to modify without changing code

**How it's used in our project:**
- Reads `config.yaml` for:
  - Groq API settings (model, tokens, temperature)
  - Database connection details
  - Cache configuration
  - Token budget limits

---

### 9. **LangChain**

**What it is:**
- A framework for building LLM-powered applications
- Provides utilities for prompts, chains, and tool integration

**Why we use it:**
- **Integration with Groq**: `langchain-groq` package simplifies API calls
- **Prompt templates**: Structured way to format prompts
- **Tool calling**: Framework for LLM to use external tools
- Works seamlessly with LangGraph

**How it's used in our project:**
- Used alongside LangGraph for agent orchestration
- Provides prompt engineering utilities in `src/llm/prompts.py`
- Handles LLM responses and parsing

---

## 🔄 How Everything Works Together

Here's the flow when a user asks a question:

```
User Question
    ↓
FastAPI Server (app.py)
    ↓
LangGraph Workflow (src/agent/graph.py)
    ↓
┌─────────────────────────────────────────────┐
│ Step 1: Parse Question                      │
│ - LLM identifies what tables are needed     │
│ - Uses Groq API (via langchain-groq)        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Step 2: Get Schema                          │
│ - Check Schema Cache first (save tokens!)   │
│ - If not cached, use MCP Tools to fetch     │
│ - Cache the schema for future use           │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Step 3: Generate SQL                        │
│ - LLM generates SQL query                   │
│ - Uses optimized prompts to minimize tokens │
│ - Groq API processes this                   │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Step 4: Execute SQL                         │
│ - MCP Tools execute query on MySQL          │
│ - Database does all the heavy lifting       │
│ - Returns only the results (not all data)   │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Step 5: Format Answer                       │
│ - LLM converts SQL results to natural text  │
│ - Uses minimal tokens for formatting        │
└─────────────────────────────────────────────┘
    ↓
FastAPI Response
    ↓
Web Interface (HTML/JavaScript)
    ↓
User sees answer + token count
```

---

## 💡 Why This Architecture?

### Token Efficiency
- **LangGraph** ensures we only call the LLM when absolutely necessary
- **Schema Cache** avoids repeated token usage for the same information
- **MCP Tools** let the database do computations (0 tokens) instead of the LLM

### Modularity
- Each component has a single responsibility
- Easy to swap out parts (e.g., use PostgreSQL instead of MySQL)
- Can add new features without rewriting everything

### Scalability
- FastAPI can handle multiple concurrent users
- Cache reduces load on both LLM and database
- Token tracking prevents accidental budget overruns

### Developer Experience
- YAML config is easy to modify
- Environment variables keep secrets safe
- Clear separation of concerns makes debugging easier

---

## 📊 Component Dependencies

```
┌─────────────────────────────────────────────┐
│           User Interface (Web)              │
│              FastAPI + HTML                 │
└──────────────────┬──────────────────────────┘
                   ↓
┌──────────────────────────────────────────────┐
│         LangGraph Workflow Engine            │
│         (Orchestrates everything)            │
└──────────┬───────────────────────────────────┘
           ↓
     ┌─────────────────┐
     │  Three Core     │
     │  Components:    │
     └─────────────────┘
           ↓
  ┌────────┴────────┬────────────────┐
  ↓                 ↓                ↓
┌──────────┐  ┌──────────┐  ┌─────────────┐
│   Groq   │  │   MCP    │  │   Schema    │
│  Client  │  │  Tools   │  │   Cache     │
│  (LLM)   │  │  (DB)    │  │  (Memory)   │
└──────────┘  └──────────┘  └─────────────┘
      ↓             ↓
┌──────────┐  ┌──────────┐
│   Groq   │  │  MySQL   │
│   API    │  │ Database │
│ (Cloud)  │  │ (Local)  │
└──────────┘  └──────────┘
```

---

## 📝 Summary

This project brings together:

1. **LangGraph** - To orchestrate a multi-step AI workflow
2. **Groq API** - To provide fast, affordable LLM capabilities
3. **MCP Tools** - To safely interact with the database
4. **MySQL** - To store and query structured data
5. **FastAPI** - To provide a web interface
6. **Schema Cache** - To minimize token usage
7. **LangChain** - To integrate everything smoothly

Each component serves a specific purpose, and together they create an intelligent agent that can answer database questions using **98.5% fewer tokens** than traditional approaches!

---

*Have more questions about the project? Just ask!* 🚀
