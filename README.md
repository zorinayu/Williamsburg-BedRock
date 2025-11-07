# Williamsburg-BedRock

# 🧠 Interview Code Lens + Interactive Code Visualizer

> A zero-setup viewer that instantly reveals **code structure**, **dependencies**, **function inventory**, and **logic flow** — complete with explanations, language conversion, and AI-powered insights.

---

## 🚀 Overview

**Interview Code Lens** is an AI-augmented **code visualizer and analyzer** that transforms any uploaded code file into an interactive, explainable diagram.  
It helps developers, interviewers, and reviewers understand *what’s inside* a codebase — without running anything.

**Core Idea**
- Upload any code file (40+ programming languages supported)
- Instantly see structure, dependencies, and metrics
- Explore visual flowcharts with AI explanations and translation
- Get a 10-second snapshot of coding style, complexity, and maintainability
- Cross-language code conversion powered by AWS Bedrock AI

---

## 🧩 Key Features

### 🔍 1. Instant Code Snapshot
- **Language auto-detection** (40+ programming languages)
- **Dependency list** (imports / libraries)
- **Lines of code (LOC)** & **function count**
- **Function inventory:** name + one-line purpose (AI-generated if docstring missing)
- **Style DNA:** quick maintainability & readability score (A–F)

### 🧠 2. Interactive Flow Visualizer
- Clickable **flowchart** of modules, classes, and functions  
- Drill down into any node:
  - Plain-English explanation of purpose & logic
  - Input/output summary, time complexity, and side-effects
  - **Cross-language conversion** with AI-powered translation
- Visual "risk heatmap" overlays highlight complex or unsafe areas

### 🌐 3. Multi-Language Support & Code Conversion
**Supported Languages (40+):**
- **Popular Languages:** Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust
- **Web Technologies:** HTML, CSS, JSX, TSX, Vue
- **Scripting:** Ruby, PHP, Swift, Kotlin, Scala, R
- **Shell Scripts:** Bash, Zsh, PowerShell, Shell
- **Data Formats:** JSON, YAML, XML, Markdown
- **Mobile:** Objective-C, Objective-C++, Swift, Kotlin
- **And more...**

**AI-Powered Code Conversion:**
- Convert functions between any supported languages
- Preserve logic and functionality during translation
- Supported conversion targets: Java, C++, Rust, C, JavaScript, and more
- Powered by AWS Bedrock AI for accurate translations

### 💬 4. AI-Enhanced Insights
Powered by **Amazon Bedrock (Claude 3 Sonnet / Titan)**:
- Generates concise, grounded function summaries for any language
- Auto-translates code between 40+ programming languages
- Language-aware analysis that understands syntax and patterns
- Answers semantic questions ("Where is file I/O handled?")
- Creates **interview-ready reviewer questions** for candidate evaluation

### 🧑‍💻 5. Use Cases
| Scenario | How it Helps |
|-----------|---------------|
| **Interview Screening** | Instantly understand candidate submissions |
| **Code Reviews** | Get “what’s inside” snapshots before deep dives |
| **Onboarding** | Visualize unfamiliar modules and function flows |
| **Education** | Learn by comparing cross-language translations |
| **Multi-Language Projects** | Understand and convert code across different tech stacks |
| **Code Migration** | Translate legacy code to modern languages with AI assistance |

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
User Upload → Language Detection → Parser (AST/Regex) → Snapshot Metrics → 
Bedrock AI Analysis → Visual Graph → Interactive Exploration
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ (Python 3.10+ recommended)
- AWS Account with Bedrock access (for AI features)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zorinayu/Williamsburg-BedRock.git
   cd Williamsburg-BedRock
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   pip install -r requirements.txt
   
   # Install Web app dependencies
   cd Web
   pip install -r requirements.txt
   ```

3. **Configure AWS Bedrock** (Optional, for AI features)
   - Create a `.env` file in the root directory
   - Add your AWS credentials:
     ```env
     AWS_ACCESS_KEY_ID=your_access_key
     AWS_SECRET_ACCESS_KEY=your_secret_key
     AWS_DEFAULT_REGION=us-west-2
     ```

4. **Run the application**
   ```bash
   cd Web
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501` (or the URL shown in terminal)

### Usage

1. **Upload a code file** - Drag and drop or browse any code file (40+ languages supported)
2. **View instant analysis** - See language, dependencies, functions, and code structure
3. **Enable AI features** (optional) - Toggle "Enhance with AI" for:
   - AI-generated function summaries
   - Cross-language code conversion
   - Enhanced code analysis
4. **Explore code structure** - Click on functions to see details and convert to other languages

---









---

## 📋 Detailed Features

### Code Analysis
- **Automatic Language Detection**: Identifies 40+ programming languages from file extension and code patterns
- **Dependency Extraction**: Parses imports, requires, includes across multiple languages
- **Function Extraction**: Identifies functions, methods, and procedures with parameter analysis
- **Code Structure Visualization**: Interactive tree view of classes, functions, and their relationships

### AI-Powered Features
- **Smart Function Summaries**: Generates concise descriptions when docstrings are missing
- **Cross-Language Conversion**: Convert functions between supported languages while preserving logic
- **Language-Aware Analysis**: Understands syntax patterns and idioms for each language
- **Semantic Understanding**: AI-powered insights into code purpose and behavior

### Supported File Types
The application automatically detects and analyzes:
- **Source Code**: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.go`, `.rs`, `.cs`, `.rb`, `.php`, `.swift`, `.kt`, and more
- **Web Files**: `.html`, `.css`, `.jsx`, `.tsx`, `.vue`
- **Scripts**: `.sh`, `.bash`, `.zsh`, `.ps1`
- **Config Files**: `.json`, `.yaml`, `.yml`, `.xml`
- **Documentation**: `.md`

---

## 🔧 Technical Details

### Core Components

1. **File Parser**: 
   - AST-based analysis for Python (using `ast` module)
   - Regex-based parsing for 40+ other languages
   - Pattern matching for functions, classes, and dependencies

2. **Language Detection**: 
   - File extension mapping (40+ extensions)
   - Content-based pattern recognition
   - Fallback to content analysis when extension is unknown

3. **Dependency Extractor**: 
   - Multi-language import statement parsing
   - Supports: `import`, `require`, `include`, `use`, `using`, etc.

4. **Function Analyzer**: 
   - Extracts function definitions across all supported languages
   - Identifies parameters and signatures
   - Generates code snippets for each function

5. **AI Enhancement** (Optional): 
   - AWS Bedrock integration for intelligent analysis
   - Function summary generation
   - Cross-language code conversion

### Technical Stack

* **Frontend**: 
  - Streamlit web interface
  - Multi-language syntax highlighting
  - Interactive code visualization with Graphviz

* **Backend**: 
  - Python AST parsing (for Python files)
  - Regex-based parsing (for 40+ other languages)
  - AWS Bedrock SDK integration

* **AI Integration**: 
  - AWS Bedrock (Titan Text Lite) for code conversion
  - Language-aware prompt engineering
  - Context-aware function analysis

* **Language Support**: 
  - Automatic detection for 40+ programming languages
  - Syntax-aware parsing and analysis
  - Cross-language compatibility

* **Deployment**: 
  - Local development with Streamlit
  - Cloud deployment ready (AWS, Heroku, etc.)

---

## 📝 Example Workflow

1. **Upload Code**: Drag and drop a `sample_code.cpp` file
2. **Automatic Detection**: System identifies it as C++ code
3. **Analysis**: Extracts functions, dependencies (`#include` statements), and structure
4. **Visualization**: Displays interactive code tree with classes and functions
5. **AI Enhancement** (if enabled): 
   - Generates summaries for each function
   - Provides conversion options to Java, Python, Rust, etc.
6. **Explore**: Click on any function to see details and convert to other languages

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is part of a Columbia University course project.

---

## 👥 Contributors

* **Haiyue Zhang** - hz2995@columbia.edu (Backend development, AWS Infrastructure)
* **Tanmay Agarwal** - ta2830@columbia.edu (Idea, AI development, Tech Integrator)
* **Shriya Shivaraman** - ss7543@columbia.edu
* **Yanxuan Yu** - yy3523@columbia.edu (Frontend development, exploring Next.js)

---

## 🔗 Related Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Python AST Module](https://docs.python.org/3/library/ast.html)

