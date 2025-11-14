import streamlit as st
import os
import sys
import hashlib
import streamlit.components.v1 as components

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
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for interview interface
interview_style = """
    <style>
    .stDeployButton {display: none;}
    
    /* Video container styling */
    .video-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .interview-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    .code-upload-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border: 2px dashed #dee2e6;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    </style>
"""
st.markdown(interview_style, unsafe_allow_html=True)

# Show login form if user clicked login button
if st.session_state.show_login:
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_form()
    st.stop()

# Main content - Interview Interface
# Header with title and login
header_col1, header_col2 = st.columns([8, 1])
with header_col1:
    st.markdown('<h1 class="main-title">💼 Interview Code Lens</h1>', unsafe_allow_html=True)
    st.markdown("**Live Coding Interview Platform** - Real-time code analysis and AI-powered insights")
with header_col2:
    if st.session_state.authenticated:
        if st.button("🚪 Logout", key="logout_top", use_container_width=True):
            logout()
    else:
        if st.button("🔐 Login", key="login_top", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

# Show login status in sidebar
with st.sidebar:
    st.markdown("### 👤 Interview Status")
    if st.session_state.authenticated:
        st.success(f"✅ **Logged in as:** {st.session_state.username}")
        st.info("🎯 **Role:** Interviewer")
    else:
        st.info("💡 Login to access full interview features")
    
    st.markdown("---")
    st.markdown("### 📊 Session Info")
    st.caption("Interview ID: #INT-2024-001")
    st.caption("Duration: Active")

analyzer = CodeAnalyzer()
bedrock = BedrockHelper()

# Get available models
available_models = bedrock.get_available_models()
model_options = {f"{m['modelName']} ({m['providerName']})": m['modelId'] for m in available_models}

# Initialize session state for selected model (default to Titan Lite)
if 'selected_model_id' not in st.session_state:
    st.session_state.selected_model_id = 'amazon.titan-text-lite-v1'

# Initialize session state for target language
if 'target_language' not in st.session_state:
    st.session_state.target_language = 'Python'

# Main interview interface layout
left_col, right_col = st.columns([1, 2])

with left_col:
    # Video Interview Section
    st.markdown('<div class="interview-header">', unsafe_allow_html=True)
    st.markdown("### 🎥 Live Interview")
    st.markdown("</div>", unsafe_allow_html=True)
    # Real webcam video interface using browser camera & microphone (getUserMedia)
    video_placeholder = st.empty()
    with video_placeholder:
        video_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            body {
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
            #video-container {
                background: #1a1a1a;
                border-radius: 12px;
                padding: 0;
                position: relative;
                min-height: 320px;
                overflow: hidden;
                margin-bottom: 10px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            }
            #video-area {
                width: 100%;
                height: 260px;
                background: #000;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            #localVideo {
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: none;
            }
            #placeholder {
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                color: white;
            }
            .avatar {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 15px;
                box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
                animation: pulse 2s infinite;
            }
            .status-badge {
                position: absolute;
                top: 12px;
                right: 12px;
                background: rgba(0,0,0,0.65);
                padding: 6px 12px;
                border-radius: 20px;
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 0.8em;
                color: #e5e7eb;
            }
            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #ef4444;
                animation: blink 1.5s infinite;
            }
            .quality-badge {
                position: absolute;
                bottom: 12px;
                left: 12px;
                background: rgba(0,0,0,0.65);
                padding: 4px 10px;
                border-radius: 14px;
                font-size: 0.75em;
                color: #e5e7eb;
            }
            #info-bar {
                background: #2d3748;
                padding: 10px 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.85em;
                color: #e5e7eb;
            }
            #controls {
                display: flex;
                gap: 8px;
                margin-top: 6px;
            }
            .btn {
                flex: 1;
                border: none;
                padding: 8px 10px;
                border-radius: 999px;
                cursor: pointer;
                font-size: 0.85em;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
                background: #111827;
                color: #e5e7eb;
            }
            .btn-primary {
                background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
            }
            .btn-danger {
                background: #b91c1c;
            }
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .volume-row {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-top: 6px;
                font-size: 0.8em;
                color: #9ca3af;
            }
            .volume-row input[type=range] {
                flex: 1;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.05); opacity: 0.9; }
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            </style>
        </head>
        <body>
            <div id="video-container">
                <div id="video-area">
                    <video id="localVideo" autoplay playsinline muted></video>
                    <div id="placeholder">
                        <div class="avatar">
                            <span style="font-size: 46px;">👤</span>
                        </div>
                        <p style="margin: 0; font-size: 1.05em;">Click <strong>Start Camera</strong> to begin</p>
                        <p style="margin: 4px 0 0; font-size: 0.85em; opacity: 0.8;">
                            Your browser will ask for camera & microphone permission
                        </p>
                    </div>
                    <div class="status-badge" id="statusBadge">
                        <span class="status-dot" id="statusDot"></span>
                        <span id="statusText">Offline</span>
                    </div>
                    <div class="quality-badge" id="qualityBadge">
                        HD 1080p
                    </div>
                </div>
                <div id="info-bar">
                    <div>📹 Candidate Video Stream</div>
                    <div id="audioIndicator">🎤 Audio: On</div>
                </div>
            </div>
            <div id="controls">
                <button class="btn btn-primary" id="camBtn" onclick="toggleCamera()">▶ Start Camera</button>
                <button class="btn" id="micBtn" onclick="toggleMic()" disabled>🎤 Mute</button>
                <button class="btn btn-danger" id="endBtn" onclick="endCall()" disabled>📞 End</button>
            </div>
            <div class="volume-row">
                <span>🔊 Volume</span>
                <input id="volSlider" type="range" min="0" max="100" value="70" oninput="setVolume(this.value)">
                <span id="volLabel">70%</span>
            </div>
            <script>
            let localStream = null;
            let videoOn = false;
            let micMuted = false;

            const videoEl = document.getElementById('localVideo');
            const placeholderEl = document.getElementById('placeholder');
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            const audioIndicator = document.getElementById('audioIndicator');
            const camBtn = document.getElementById('camBtn');
            const micBtn = document.getElementById('micBtn');
            const endBtn = document.getElementById('endBtn');
            const volLabel = document.getElementById('volLabel');

            async function startCamera() {
                try {
                    localStream = await navigator.mediaDevices.getUserMedia({
                        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
                        audio: true
                    });
                    videoEl.srcObject = localStream;
                    videoEl.style.display = 'block';
                    videoEl.volume = 0.7;
                    placeholderEl.style.display = 'none';
                    statusDot.style.background = '#22c55e';
                    statusText.textContent = 'Live';
                    audioIndicator.textContent = '🎤 Audio: On';
                    camBtn.textContent = '⏸ Stop Camera';
                    videoOn = true;
                    micBtn.disabled = false;
                    endBtn.disabled = false;
                } catch (err) {
                    console.error('Error accessing camera/microphone:', err);
                    alert('Unable to access camera or microphone.\\n\\nPlease check browser permissions and that your devices are not in use by another app.\\n\\nError: ' + err.message);
                }
            }

            function stopCamera() {
                if (localStream) {
                    localStream.getTracks().forEach(t => t.stop());
                }
                localStream = null;
                videoEl.srcObject = null;
                videoEl.style.display = 'none';
                placeholderEl.style.display = 'flex';
                statusDot.style.background = '#ef4444';
                statusText.textContent = 'Offline';
                audioIndicator.textContent = '🎤 Audio: Off';
                camBtn.textContent = '▶ Start Camera';
                videoOn = false;
                micMuted = false;
                micBtn.disabled = true;
                endBtn.disabled = true;
            }

            function toggleCamera() {
                if (!videoOn) {
                    startCamera();
                } else {
                    stopCamera();
                }
            }

            function toggleMic() {
                if (!localStream) return;
                localStream.getAudioTracks().forEach(t => { t.enabled = !t.enabled; });
                micMuted = !micMuted;
                if (micMuted) {
                    audioIndicator.textContent = '🎤 Audio: Muted';
                    micBtn.textContent = '🎤 Unmute';
                } else {
                    audioIndicator.textContent = '🎤 Audio: On';
                    micBtn.textContent = '🎤 Mute';
                }
            }

            function endCall() {
                stopCamera();
                alert('Interview session ended.');
            }

            function setVolume(v) {
                if (videoEl) {
                    videoEl.volume = v / 100;
                }
                if (volLabel) {
                    volLabel.textContent = v + '%';
                }
            }
            </script>
        </body>
        </html>
        """
        # Increase height so that the volume slider and labels are fully visible
        components.html(video_html, height=430, scrolling=False)

    # Interview controls (high-level status only; actual media control is handled in the embedded component)
    st.markdown("### 🎛️ Interview Controls")
    control_col1, control_col2, control_col3 = st.columns(3)
    with control_col1:
        st.button("📝 Add Note", use_container_width=True, key="note_btn")
    with control_col2:
        st.button("⏱ Mark Timestamp", use_container_width=True, key="timestamp_btn")
    with control_col3:
        if st.button("📞 End Session", use_container_width=True, key="session_end_btn", type="primary"):
            st.warning("Interview session marked as ended (video can still be controlled in the panel above).")
    
    st.markdown("---")
    
    # Code Upload Section
    st.markdown('<div class="code-upload-section">', unsafe_allow_html=True)
    st.markdown("### 📁 Candidate Code Submission")
    uploaded_file = st.file_uploader(
        "Upload candidate's code file", 
        type=None, 
        accept_multiple_files=False,
        help="Candidate can submit their code solution here"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file:
        st.success(f"✅ **Received:** {uploaded_file.name}")
        st.caption(f"📊 File size: {len(uploaded_file.read())} bytes")
        uploaded_file.seek(0)  # Reset file pointer
    
    # AI Enhancement section
    st.markdown("---")
    st.markdown("### 🤖 AI Analysis Tools")
    use_ai = st.toggle("✨ Enable AI Code Analysis", value=False, help="Use AI to analyze and convert code")
    
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
            st.caption(f"🤖 Provider: {selected_model['providerName']}")

with right_col:
    # Code Analysis Panel
    if not uploaded_file:
        st.markdown("### 📋 Code Analysis Panel")
        st.info("👈 **Waiting for code submission...** Upload candidate's code file on the left to begin analysis.")
        
        # Show placeholder analysis interface
        st.markdown("---")
        st.markdown("#### 📊 Analysis Preview")
        placeholder_col1, placeholder_col2, placeholder_col3, placeholder_col4 = st.columns(4)
        with placeholder_col1:
            st.metric("Language", "-")
        with placeholder_col2:
            st.metric("Libraries", "-")
        with placeholder_col3:
            st.metric("Lines", "-")
        with placeholder_col4:
            st.metric("Functions", "-")
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
        
        # Language display with target language selector (if AI is enabled)
        detected_language = analysis.get('language', 'Python')
        if use_ai:
            # Show language metric with dropdown selector
            with metric_col1:
                st.metric("Language", detected_language)
                # Available target languages - 40+ languages comprehensive list
                available_target_languages = [
                    # Mainstream Languages (7)
                    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
                    # Modern Systems Languages (6)
                    "Rust", "Go", "Swift", "Kotlin", "Dart", "Zig",
                    # Functional & Scripting (8)
                    "Ruby", "PHP", "Perl", "Lua", "Scala", "Haskell", "F#", "Elixir",
                    # Data Science & Scientific (4)
                    "R", "MATLAB", "Julia", "Fortran",
                    # Web & Frontend (6)
                    "HTML", "CSS", "Vue", "Svelte", "CoffeeScript", "Elm",
                    # Systems & Low-level (4)
                    "Assembly", "Nim", "Crystal", "D",
                    # Legacy & Enterprise (3)
                    "COBOL", "Pascal", "Ada",
                    # Other Popular (5)
                    "Shell", "Bash", "PowerShell", "SQL", "Groovy",
                    # Functional & Logic (3)
                    "Clojure", "Erlang", "OCaml"
                ]
                # Normalize language names for comparison (handle variations)
                language_normalization = {
                    'c++': 'c++', 'cpp': 'c++', 'cxx': 'c++',
                    'c#': 'c#', 'csharp': 'c#', 'cs': 'c#',
                    'javascript': 'javascript', 'js': 'javascript',
                    'typescript': 'typescript', 'ts': 'typescript',
                    'objective-c': 'objective-c', 'objc': 'objective-c',
                    'objective-c++': 'objective-c++', 'objcpp': 'objective-c++',
                    'shell': 'shell', 'bash': 'shell', 'sh': 'shell',
                    'yaml': 'yaml', 'yml': 'yaml',
                    'f#': 'f#', 'fsharp': 'f#',
                    'assembly': 'assembly', 'asm': 'assembly',
                    'cobol': 'cobol', 'cbl': 'cobol',
                    'pascal': 'pascal', 'pas': 'pascal',
                    'groovy': 'groovy', 'gvy': 'groovy',
                    'coffeescript': 'coffeescript', 'coffee': 'coffeescript'
                }
                
                # Normalize detected language
                detected_lang_normalized = detected_language.lower()
                if detected_lang_normalized in language_normalization:
                    detected_lang_normalized = language_normalization[detected_lang_normalized]
                
                # Remove current language from options (case-insensitive)
                target_options = []
                for lang in available_target_languages:
                    lang_normalized = lang.lower()
                    if lang_normalized in language_normalization:
                        lang_normalized = language_normalization[lang_normalized]
                    if lang_normalized != detected_lang_normalized:
                        target_options.append(lang)
                
                if not target_options:
                    target_options = available_target_languages
                
                # Find current selection index
                current_index = 0
                if st.session_state.target_language in target_options:
                    current_index = target_options.index(st.session_state.target_language)
                
                selected_target = st.selectbox(
                    "Convert to:",
                    options=target_options,
                    index=current_index,
                    key="target_language_selector",
                    label_visibility="visible"
                )
                # Clear conversion cache if target language changed
                if st.session_state.target_language != selected_target:
                    # Clear all conversion caches
                    keys_to_remove = [key for key in st.session_state.keys() if key.startswith("converted_")]
                    for key in keys_to_remove:
                        del st.session_state[key]
                st.session_state.target_language = selected_target
        else:
            metric_col1.metric("Language", detected_language)
        
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
                            # Get target language from session state
                            target_lang = st.session_state.target_language
                            
                            # Only show two tabs: original language and target language
                            original_lang_display = detected_language.title()
                            tab_languages = [original_lang_display, target_lang]
                            
                            tabs = st.tabs(tab_languages)
                            
                            # First tab - original language
                            with tabs[0]:
                                st.code(func_code, language=code_lang)
                            
                            # Second tab - converted language
                            with tabs[1]:
                                # Use a unique key for each function to cache the conversion
                                conversion_key = f"converted_{func_name}_{target_lang}_{hash(func_code)}"
                                
                                if conversion_key not in st.session_state:
                                    # Convert the code
                                    with st.spinner(f"Converting {func_name} to {target_lang}..."):
                                        converted_code = bedrock.convert_function_to_language(
                                            func_code, 
                                            target_lang, 
                                            detected_language.title(),
                                            st.session_state.selected_model_id
                                        )
                                        st.session_state[conversion_key] = converted_code
                                
                                converted_code = st.session_state[conversion_key]
                                
                                # Check if result is an error
                                if converted_code.startswith("MODEL_ERROR:"):
                                    error_msg = converted_code.replace("MODEL_ERROR:", "").strip()
                                    st.error("⚠️ **Model Error**")
                                    st.warning(error_msg)
                                    st.info("💡 **Suggestion**: Please try selecting a different model from the AI Enhancement section (e.g., switch to Titan Text Lite). Some models may have limitations with certain code patterns or languages.")
                                elif converted_code.startswith("HTTP_ERROR:"):
                                    error_msg = converted_code.replace("HTTP_ERROR:", "").strip()
                                    st.error("⚠️ **Connection Error**")
                                    st.warning(error_msg)
                                    st.info("💡 **Suggestion**: This is a network or authentication issue, not a model problem. Please check your API key and network connection.")
                                elif converted_code.startswith("SYSTEM_ERROR:"):
                                    error_msg = converted_code.replace("SYSTEM_ERROR:", "").strip()
                                    st.error("⚠️ **System Error**")
                                    st.warning(error_msg)
                                    st.info("💡 **Suggestion**: Please try again or contact support if the problem persists.")
                                elif converted_code.startswith("// Error:") or converted_code.startswith("Error:"):
                                    st.error(converted_code.replace("// Error:", "").replace("Error:", "").strip())
                                else:
                                    # Map target language to syntax highlighting (40+ languages)
                                    target_lang_map = {
                                        # Mainstream Languages
                                        "Python": "python", "Java": "java", "JavaScript": "javascript",
                                        "TypeScript": "typescript", "C": "c", "C++": "cpp", "C#": "csharp",
                                        # Modern Systems Languages
                                        "Rust": "rust", "Go": "go", "Swift": "swift", 
                                        "Kotlin": "kotlin", "Dart": "dart", "Zig": "zig",
                                        # Functional & Scripting
                                        "Ruby": "ruby", "PHP": "php", "Perl": "perl", 
                                        "Lua": "lua", "Scala": "scala", "Haskell": "haskell",
                                        "F#": "fsharp", "Elixir": "elixir",
                                        # Data Science & Scientific
                                        "R": "r", "MATLAB": "matlab", "Julia": "julia", "Fortran": "fortran",
                                        # Web & Frontend
                                        "HTML": "html", "CSS": "css", "Vue": "vue", 
                                        "Svelte": "svelte", "CoffeeScript": "coffeescript", "Elm": "elm",
                                        # Systems & Low-level
                                        "Assembly": "asm", "Nim": "nim", "Crystal": "crystal", "D": "d",
                                        # Legacy & Enterprise
                                        "COBOL": "cobol", "Pascal": "pascal", "Ada": "ada",
                                        # Other Popular
                                        "Shell": "bash", "Bash": "bash", "PowerShell": "powershell", 
                                        "SQL": "sql", "Groovy": "groovy",
                                        # Functional & Logic
                                        "Clojure": "clojure", "Erlang": "erlang", "OCaml": "ocaml"
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
            