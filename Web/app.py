import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from code_analyzer import CodeAnalyzer
from bedrock_helper import BedrockHelper

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

st.set_page_config(page_title="Interview Code Lens", page_icon="👀", layout="wide")

st.title("👀 Interview Code Lens")
st.markdown("**Instant Code Snapshot** - Get a 10-second overview of coding style and tech stack")

analyzer = CodeAnalyzer()
bedrock = BedrockHelper()

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("📁 Upload Code File")
    uploaded_file = st.file_uploader("Choose a Python file (.py)", type=["py"])
    use_ai = st.toggle("✨ Enhance with AI", value=False)
    if uploaded_file:
        st.success(f"✅ File loaded: {uploaded_file.name}")

with right_col:
    if not uploaded_file:
        st.info("👈 Upload a `.py` file on the left to see instant insights.")
    else:
        code_bytes = uploaded_file.read()
        code_text = code_bytes.decode("utf-8", errors="ignore")
        
        with st.spinner("Analyzing code..."):
            analysis = analyzer.analyze(code_text, uploaded_file.name)
            if use_ai and analysis['functions']:
                with st.spinner("Enhancing function summaries with AI..."):
                    analysis = bedrock.enhance_analysis(analysis)
        
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
                        
                        # Language conversion tabs
                        if use_ai:
                            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Python", "Java", "C++", "Rust", "C", "JavaScript"])
                            
                            with tab1:
                                st.code(func_code, language="python")
                            
                            with tab2:
                                if st.button(f"Convert {func_name} to Java", key=f"java_{func_name}"):
                                    with st.spinner("Converting to Java..."):
                                        java_code = bedrock.convert_function_to_language(func_code, "Java")
                                        st.code(java_code, language="java")
                            
                            with tab3:
                                if st.button(f"Convert {func_name} to C++", key=f"cpp_{func_name}"):
                                    with st.spinner("Converting to C++..."):
                                        cpp_code = bedrock.convert_function_to_language(func_code, "C++")
                                        st.code(cpp_code, language="cpp")
                            
                            with tab4:
                                if st.button(f"Convert {func_name} to Rust", key=f"rust_{func_name}"):
                                    with st.spinner("Converting to Rust..."):
                                        rust_code = bedrock.convert_function_to_language(func_code, "Rust")
                                        st.code(rust_code, language="rust")
                            
                            with tab5:
                                if st.button(f"Convert {func_name} to C", key=f"c_{func_name}"):
                                    with st.spinner("Converting to C..."):
                                        c_code = bedrock.convert_function_to_language(func_code, "C")
                                        st.code(c_code, language="c")
                            
                            with tab6:
                                if st.button(f"Convert {func_name} to JavaScript", key=f"js_{func_name}"):
                                    with st.spinner("Converting to JavaScript..."):
                                        js_code = bedrock.convert_function_to_language(func_code, "JavaScript")
                                        st.code(js_code, language="javascript")
                        else:
                            st.code(func_code, language="python")
                else:
                    # Backward compatibility
                    func_name, func_summary = func_data
                    with st.expander(f"`{func_name}`", expanded=False):
                        st.write(func_summary)
        else:
            st.write("No functions found.")
        
        st.subheader("📝 Source Code")
        with st.expander("Click to view source code", expanded=False):
            st.code(code_text, language="python")