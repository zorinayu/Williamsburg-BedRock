# Williamsburg-BedRock

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

