import streamlit as st
import os
import sys
import hashlib

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from code_analyzer import CodeAnalyzer
from bedrock_helper import BedrockHelper

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Simple user database (in production, use a proper database)
USERS = {
    'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
    'user': hashlib.sha256('user123'.encode()).hexdigest(),
}

def authenticate(username, password):
    """Authenticate user"""
    if not username or not password:
        return False
    username = username.strip()
    if username in USERS:
        password_hash = hashlib.sha256(password.strip().encode()).hexdigest()
        if USERS[username] == password_hash:
            return True
    return False

def login_form():
    """Display login form"""
    st.header("🔐 Login")
    st.markdown("---")
    
    # Show test credentials
    with st.expander("ℹ️ Test Credentials", expanded=True):
        st.code("""
Username: admin
Password: admin123

Username: user  
Password: user123
        """)
    
    username = st.text_input("Username", key="login_username", placeholder="Enter username")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
    
    col1, col2 = st.columns(2)
    with col1:
        login_btn = st.button("Login", use_container_width=True, type="primary")
    with col2:
        cancel_btn = st.button("Cancel", use_container_width=True)
    
    if login_btn:
        if not username or not password:
            st.error("Please enter both username and password")
        elif authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.show_login = False
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
            st.info("💡 Hint: Check the test credentials above")
    
    if cancel_btn:
        st.session_state.show_login = False
        st.rerun()

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.show_login = False
    st.rerun()

def format_tree_text(tree):
    """Format code tree as text"""
    if not tree:
        return "📄 (Simple script - no classes or functions)"
    
    lines = ["📄 Module"]
    items_by_parent = {}
    root_items = []
    
    for item in tree:
        if item['parent']:
            if item['parent'] not in items_by_parent:
                items_by_parent[item['parent']] = []
            items_by_parent[item['parent']].append(item)
        else:
            root_items.append(item)
    
    def render_item(item, prefix="", is_last=True):
        connector = "└─ " if is_last else "├─ "
        if item['type'] == 'class':
            lines.append(f"{prefix}{connector}📦 Class: {item['name']}")
            new_prefix = prefix + ("   " if is_last else "│  ")
            children = items_by_parent.get(item['name'], [])
            for i, child in enumerate(children):
                render_item(child, new_prefix, i == len(children) - 1)
        elif item['type'] == 'function':
            icon = "🔧" if item['parent'] else "⚙️"
            parent_prefix = f"{item['parent']}." if item['parent'] else ""
            args_str = f"({', '.join(item['args'])})" if item['args'] else "()"
            lines.append(f"{prefix}{connector}{icon} {parent_prefix}{item['name']}{args_str}")
    
    for i, item in enumerate(root_items):
        render_item(item, "", i == len(root_items) - 1)
    
    return "\n".join(lines)

st.set_page_config(
    page_title="Interview Code Lens", 
    page_icon="👀", 
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide the default Streamlit menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    button[title="View app source"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Show login form if user clicked login button
if st.session_state.show_login:
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_form()
    st.stop()

# Main content - always shown (login is optional)
# Login/Logout button in top right corner
col1, col2 = st.columns([10, 1])
with col1:
    st.title("👀 Interview Code Lens")
with col2:
    if st.session_state.authenticated:
        if st.button("🚪 Logout", key="logout_top"):
            logout()
    else:
        if st.button("🔐 Login", key="login_top"):
            st.session_state.show_login = True
            st.rerun()

st.markdown("**Instant Code Snapshot** - Get a 10-second overview of coding style and tech stack")

# Show login status in sidebar
with st.sidebar:
    if st.session_state.authenticated:
        st.success(f"✅ Logged in as: **{st.session_state.username}**")
    else:
        st.info("💡 Login is optional - click Login button to access additional features")

analyzer = CodeAnalyzer()
bedrock = BedrockHelper()

# Get available models
available_models = bedrock.get_available_models()
model_options = {f"{m['modelName']} ({m['providerName']})": m['modelId'] for m in available_models}

# Initialize session state for selected model (default to Titan Lite)
if 'selected_model_id' not in st.session_state:
    st.session_state.selected_model_id = 'amazon.titan-text-lite-v1'

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("📁 Upload Code File")
    uploaded_file = st.file_uploader("Choose a code file", type=None, accept_multiple_files=False)
    
    # AI Enhancement section
    st.markdown("---")
    st.subheader("🤖 AI Enhancement")
    use_ai = st.toggle("✨ Enable AI Enhancement", value=False)
    
    selected_model_display = None
    if use_ai:
        # Find default model index (Titan Lite)
        default_index = 0
        for i, (key, model_id) in enumerate(model_options.items()):
            if model_id == st.session_state.selected_model_id:
                default_index = i
                break
        
        # Model selection dropdown
        selected_model_display = st.selectbox(
            "Select Bedrock Model:",
            options=list(model_options.keys()),
            index=default_index,
            help="Choose which AWS Bedrock model to use for AI enhancement"
        )
        st.session_state.selected_model_id = model_options[selected_model_display]
        
        # Show model info
        selected_model = next((m for m in available_models if m['modelId'] == st.session_state.selected_model_id), None)
        if selected_model:
            st.caption(f"Provider: {selected_model['providerName']}")
    
    if uploaded_file:
        st.success(f"✅ File loaded: {uploaded_file.name}")

with right_col:
    if not uploaded_file:
        st.info("👈 Upload any code file on the left to see instant insights.")
    else:
        code_bytes = uploaded_file.read()
        code_text = code_bytes.decode("utf-8", errors="ignore")
        
        with st.spinner("Analyzing code..."):
            analysis = analyzer.analyze(code_text, uploaded_file.name)
            if use_ai and analysis['functions']:
                with st.spinner(f"Enhancing function summaries with AI ({selected_model_display if use_ai else ''})..."):
                    analysis = bedrock.enhance_analysis(analysis, st.session_state.selected_model_id)
        
        st.subheader("📊 Overview")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metric_col1.metric("Language", analysis['language'])
        metric_col2.metric("Libraries", len(analysis['libraries']))
        metric_col3.metric("Lines of Code", analysis['loc'])
        metric_col4.metric("Functions", len(analysis['functions']))
        
        st.subheader("📚 Libraries Used")
        if analysis['libraries']:
            st.write(", ".join(sorted(analysis['libraries'])))
        else:
            st.write("— No external libraries detected")
        
        st.subheader("🌳 Code Structure Tree")
        if analysis.get('tree_graphviz'):
            try:
                st.graphviz_chart(analysis['tree_graphviz'])
            except ImportError:
                st.warning("Graphviz not installed. Install with: pip install graphviz")
                tree = analysis.get('code_tree', [])
                if tree:
                    tree_text = format_tree_text(tree)
                    st.code(tree_text, language="text")
                else:
                    st.write("📄 (Simple script - no classes or functions)")
            except Exception as e:
                st.error(f"Error rendering tree: {str(e)}")
                tree = analysis.get('code_tree', [])
                if tree:
                    tree_text = format_tree_text(tree)
                    st.code(tree_text, language="text")
        else:
            st.write("📄 (Simple script - no classes or functions)")
        
        st.subheader("🔧 Function Inventory")
        if analysis['functions']:
            for func_data in analysis['functions']:
                if len(func_data) == 3:
                    func_name, func_summary, func_code = func_data
                    with st.expander(f"`{func_name}`", expanded=False):
                        st.write(func_summary)
                        
                        # Get language for syntax highlighting
                        detected_language = analysis.get('language', 'python').lower()
                        # Map language names to streamlit code language identifiers
                        lang_map = {
                            'python': 'python',
                            'javascript': 'javascript',
                            'typescript': 'typescript',
                            'java': 'java',
                            'c++': 'cpp',
                            'c': 'c',
                            'go': 'go',
                            'rust': 'rust',
                            'c#': 'csharp',
                            'ruby': 'ruby',
                            'php': 'php',
                            'swift': 'swift',
                            'kotlin': 'kotlin',
                        }
                        code_lang = lang_map.get(detected_language, 'text')
                        
                        # Language conversion tabs
                        if use_ai:
                            # Define all available languages
                            all_languages = ["Python", "Java", "C++", "Rust", "C", "JavaScript"]
                            
                            # Remove current language and add it as first tab
                            target_languages = [lang for lang in all_languages if lang.lower() != detected_language]
                            tab_languages = [detected_language.title()] + target_languages
                            
                            tabs = st.tabs(tab_languages)
                            
                            # First tab - original language
                            with tabs[0]:
                                st.code(func_code, language=code_lang)
                            
                            # Conversion tabs
                            for i, target_lang in enumerate(target_languages, 1):
                                with tabs[i]:
                                    if st.button(f"Convert {func_name} to {target_lang}", key=f"{target_lang.lower()}_{func_name}"):
                                        with st.spinner(f"Converting to {target_lang}..."):
                                            converted_code = bedrock.convert_function_to_language(
                                                func_code, 
                                                target_lang, 
                                                detected_language.title(),
                                                st.session_state.selected_model_id if use_ai else 'amazon.titan-text-lite-v1'
                                            )
                                            
                                            # Check if result is an error
                                            if converted_code.startswith("// Error:") or converted_code.startswith("Error:"):
                                                st.error(converted_code.replace("// Error:", "").replace("Error:", "").strip())
                                            else:
                                                # Map target language to syntax highlighting
                                                target_lang_map = {
                                                    "Python": "python", "Java": "java", "C++": "cpp", 
                                                    "Rust": "rust", "C": "c", "JavaScript": "javascript"
                                                }
                                                st.code(converted_code, language=target_lang_map.get(target_lang, "text"))
                        else:
                            st.code(func_code, language=code_lang)
                else:
                    # Backward compatibility
                    func_name, func_summary = func_data
                    with st.expander(f"`{func_name}`", expanded=False):
                        st.write(func_summary)
        else:
            st.write("No functions found.")
        
        st.subheader("📝 Source Code")
        with st.expander("Click to view source code", expanded=False):
            # Get language for syntax highlighting
            detected_language = analysis.get('language', 'python').lower()
            lang_map = {
                'python': 'python',
                'javascript': 'javascript',
                'typescript': 'typescript',
                'java': 'java',
                'c++': 'cpp',
                'c': 'c',
                'go': 'go',
                'rust': 'rust',
                'c#': 'csharp',
                'ruby': 'ruby',
                'php': 'php',
                'swift': 'swift',
                'kotlin': 'kotlin',
            }
            code_lang = lang_map.get(detected_language, 'text')
            st.code(code_text, language=code_lang)
            