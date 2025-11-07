# Williamsburg-BedRock

# 🧠 Interview Code Lens + Interactive Code Visualizer

> A zero-setup viewer that instantly reveals **code structure**, **dependencies**, **function inventory**, and **logic flow** — complete with explanations, language conversion, and AI-powered insights.

---

## 🚀 Overview

**Interview Code Lens** is an AI-augmented **code visualizer and analyzer** that transforms any uploaded code file into an interactive, explainable diagram.  
It helps developers, interviewers, and reviewers understand *what’s inside* a codebase — without running anything.

**Core Idea**
- Upload any code file (Python first, more languages next)
- Instantly see structure, dependencies, and metrics
- Explore visual flowcharts with AI explanations and translation
- Get a 10-second snapshot of coding style, complexity, and maintainability

---

## 🧩 Key Features

### 🔍 1. Instant Code Snapshot
- **Language auto-detection**
- **Dependency list** (imports / libraries)
- **Lines of code (LOC)** & **function count**
- **Function inventory:** name + one-line purpose (AI-generated if docstring missing)
- **Style DNA:** quick maintainability & readability score (A–F)

### 🧠 2. Interactive Flow Visualizer
- Clickable **flowchart** of modules, classes, and functions  
- Drill down into any node:
  - Plain-English explanation of purpose & logic
  - Input/output summary, time complexity, and side-effects
  - **Cross-language conversion** (e.g., Python → Java/TypeScript/C++)
- Visual “risk heatmap” overlays highlight complex or unsafe areas

### 💬 3. AI-Enhanced Insights
Powered by **Amazon Bedrock (Claude 3 Sonnet / Titan)**:
- Generates concise, grounded function summaries
- Auto-translates code between languages
- Answers semantic questions (“Where is file I/O handled?”)
- Creates **interview-ready reviewer questions** for candidate evaluation

### 🧑‍💻 4. Use Cases
| Scenario | How it Helps |
|-----------|---------------|
| **Interview Screening** | Instantly understand candidate submissions |
| **Code Reviews** | Get “what’s inside” snapshots before deep dives |
| **Onboarding** | Visualize unfamiliar modules and function flows |
| **Education** | Learn by comparing cross-language translations |

---

## 🧱 Architecture

### **Frontend**
- [Streamlit](https://streamlit.io) web app  
- Dual panes:  
  - **Left:** File upload  
  - **Right:** Snapshot & visualization  
- [Cytoscape.js](https://js.cytoscape.org/) or [Mermaid.js](https://mermaid.js.org) for interactive flowcharts  
- Optional Tree-sitter (WebAssembly) for multi-language parsing  

### **Backend**
- **Python + FastAPI / Streamlit Server**
- **Static analysis:** `ast`, `asttokens`, and `radon`
- **AI integration:** AWS Bedrock SDK
  - Claude 3 Sonnet → code summaries, reviewer Qs  
  - Titan Text → translation  
  - Titan Embeddings (optional) → semantic node search
- **Security:** No data persistence; code processed in-memory

### **Data Flow**
```text
User Upload → Parser → Snapshot Metrics → Bedrock Summaries → Visual Graph → Exports

```




















**Interview Code Lens**: A zero-setup viewer that instantly reveals code structure, dependencies, and function inventory from any code file. Get a 10-second snapshot of coding style and tech stack—without running anything.

## What It Does

A simple web interface with two panes:

* **Left pane**: Upload a code file (Python initially, expandable to other languages)
* **Right pane**: Instant analysis showing:
  * **Language** (auto-detected)
  * **Libraries used** (imported dependencies)
  * **Lines of code (LOC)**
  * **Function count and inventory**: Function count with detailed inventory showing name and purpose summary for each function
  * **Dynamic website**: the users can zoom in and out while also having the blocks clickable for indepth analysis.

## Why It's Useful

* **Interview screening**: Instant understanding of candidate code samples
* **Team onboarding**: Quick overview of codebase structure
* **Code reviews**: Fast "what's inside" snapshot before deep dive

## Architecture & Approach

### Core Components

1. **File Parser**: AST-based analysis for Python (extensible to other languages)
2. **Language Detection**: File extension and syntax analysis
3. **Dependency Extractor**: Parse import statements to identify libraries
4. **Function Analyzer**: Extract function definitions, names, and summaries
5. **AI Enhancement** (Optional): Use AWS Bedrock Claude to generate function summaries when docstrings are missing

### Technical Stack

* **Frontend**: Streamlit web interface
* **Backend**: Python AST parsing for code analysis
* **AI Integration**: AWS Bedrock (Claude) for intelligent function summarization
* **Deployment**: Local or cloud-based Streamlit app

## Contributors

* **Shriya Shivaraman** - ss7543@columbia.edu
* **Haiyue Zhang** - hz2995@columbia.edu
* **Tanmay Agarwal** - ta2830@columbia.edu
* **Yanxuan Yu** - yy3523@columbia.edu (Frontend development, exploring Next.js)

