# Interview Code Lens - Web Application

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open browser at http://localhost:8501

## Features

- Upload Python files for instant analysis
- View code metrics (language, libraries, LOC, functions)
- Explore function inventory with summaries
- Optional AI enhancement with AWS Bedrock

## Files

- `app.py` - Main Streamlit application
- `code_analyzer.py` - AST-based code analysis
- `bedrock_helper.py` - AWS Bedrock integration
- `sample_code.py` - Example file for testing

