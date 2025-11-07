import ast
import re
from typing import Dict, List, Tuple, Any


class CodeAnalyzer:
    # Language detection mapping
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.rs': 'Rust',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.mm': 'Objective-C++',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.zsh': 'Zsh',
        '.ps1': 'PowerShell',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.css': 'CSS',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.vue': 'Vue',
        '.xml': 'XML',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.md': 'Markdown',
    }
    
    def detect_language(self, filename: str, code_text: str = "") -> str:
        """Detect programming language from filename and optionally code content"""
        # First try extension
        for ext, lang in self.LANGUAGE_EXTENSIONS.items():
            if filename.lower().endswith(ext):
                return lang
        
        # If no match, try content-based detection
        if code_text:
            return self._detect_language_from_content(code_text)
        
        return "Unknown"
    
    def _detect_language_from_content(self, code_text: str) -> str:
        """Detect language from code content patterns"""
        code_lower = code_text.lower()
        
        # Check for language-specific patterns
        if re.search(r'\b(function|const|let|var)\s+\w+\s*=', code_text):
            if re.search(r'<script|</script>|document\.', code_text):
                return 'JavaScript'
            return 'JavaScript'
        
        if re.search(r'\bpublic\s+class\s+\w+', code_text):
            if re.search(r'@\w+|fun\s+\w+', code_text):
                return 'Kotlin'
            return 'Java'
        
        if re.search(r'#include\s*<|using\s+namespace', code_text):
            return 'C++'
        
        if re.search(r'package\s+\w+|import\s+\(', code_text):
            return 'Go'
        
        if re.search(r'fn\s+\w+|let\s+\w+:|use\s+\w+::', code_text):
            return 'Rust'
        
        if re.search(r'namespace\s+\w+|using\s+System', code_text):
            return 'C#'
        
        if re.search(r'def\s+\w+|require\s+', code_text):
            return 'Ruby'
        
        if re.search(r'<\?php|function\s+\w+\s*\(', code_text):
            return 'PHP'
        
        if re.search(r'func\s+\w+|import\s+Foundation', code_text):
            return 'Swift'
        
        return "Unknown"
    
    def count_loc(self, text: str) -> int:
        return sum(1 for line in text.splitlines() if line.strip())
    
    def parse_python(self, source: str) -> Tuple[List[str], List[Tuple[str, str, str]]]:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return [], []
        
        libraries = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    libraries.add(n.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    libraries.add(node.module.split(".")[0])
        
        functions = []
        source_lines = source.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)
                if doc:
                    summary = doc.strip().split("\n")[0]
                else:
                    arg_names = [a.arg for a in node.args.args]
                    summary = f"Function with parameters: {', '.join(arg_names)}" if arg_names else "Function with no parameters"
                
                # Extract function source code
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else len(source_lines)
                func_code = '\n'.join(source_lines[start_line:end_line])
                
                functions.append((node.name, summary, func_code))
        
        return sorted(libraries), functions
    
    def build_code_tree(self, source: str) -> List[Dict[str, Any]]:
        """Build hierarchical code structure tree"""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []
        
        structure = []
        
        def visit_node(node, parent_name="", level=0):
            if isinstance(node, ast.Module):
                for child in ast.iter_child_nodes(node):
                    visit_node(child, "", level)
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'type': 'class',
                    'name': node.name,
                    'parent': parent_name,
                    'level': level,
                    'children': []
                }
                structure.append(class_info)
                for child in ast.iter_child_nodes(node):
                    visit_node(child, node.name, level + 1)
            elif isinstance(node, ast.FunctionDef):
                func_info = {
                    'type': 'function',
                    'name': node.name,
                    'parent': parent_name,
                    'level': level,
                    'args': [a.arg for a in node.args.args if a.arg != 'self']
                }
                structure.append(func_info)
                for child in ast.iter_child_nodes(node):
                    visit_node(child, node.name, level + 1)
        
        visit_node(tree)
        return structure
    
    def generate_tree_graphviz(self, code_tree: List[Dict[str, Any]] = None, source: str = None) -> str:
        """Generate Graphviz DOT format for code tree"""
        if code_tree is None:
            if source is None:
                return None
            tree = self.build_code_tree(source)
        else:
            tree = code_tree
        
        if not tree:
            return None
        
        lines = ['digraph CodeTree {', '    rankdir=TB;', '    node [shape=box, style=rounded];']
        
        # Group items by parent
        items_by_parent = {}
        root_items = []
        
        for item in tree:
            if item['parent']:
                if item['parent'] not in items_by_parent:
                    items_by_parent[item['parent']] = []
                items_by_parent[item['parent']].append(item)
            else:
                root_items.append(item)
        
        # Create node ID mapping
        node_ids = {}
        for item in tree:
            node_id = f"{item['type']}_{item['name']}".replace('.', '_').replace('-', '_')
            node_ids[item['name']] = node_id
        
        # Add root module node
        lines.append('    Module [label="📄 Module", fillcolor="#e1f5ff", style="rounded,filled"];')
        
        # Add nodes
        for item in tree:
            node_id = node_ids[item['name']]
            if item['type'] == 'class':
                label = f"📦 {item['name']}"
                color = "#ffe1f5"
            else:
                parent_prefix = f"{item['parent']}." if item['parent'] else ""
                args_str = f"({', '.join(item['args'][:3])})" if item['args'] else "()"
                if len(item['args']) > 3:
                    args_str = args_str[:-1] + "...)"
                label = f"⚙️ {parent_prefix}{item['name']}{args_str}"
                color = "#e1ffe1"
            
            # Escape special characters in label
            label = label.replace('"', '\\"')
            lines.append(f'    {node_id} [label="{label}", fillcolor="{color}", style="rounded,filled"];')
        
        # Add edges
        for item in tree:
            node_id = node_ids[item['name']]
            if item['parent']:
                # Find parent in tree
                parent_item = next((x for x in tree if x['name'] == item['parent']), None)
                if parent_item:
                    parent_id = node_ids[item['parent']]
                    lines.append(f'    {parent_id} -> {node_id};')
                else:
                    lines.append(f'    Module -> {node_id};')
            else:
                lines.append(f'    Module -> {node_id};')
        
        lines.append('}')
        return '\n'.join(lines)
    
    def parse_generic(self, source: str, language: str) -> Tuple[List[str], List[Tuple[str, str, str]]]:
        """Generic parser for non-Python languages using regex patterns"""
        libraries = set()
        functions = []
        source_lines = source.splitlines()
        
        # Language-specific patterns
        patterns = {
            'JavaScript': [
                (r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', 'import'),
                (r'require\([\'"]([^\'"]+)[\'"]\)', 'require'),
                (r'(?:function|const|let|var)\s+(\w+)\s*[=\(]', 'function'),
            ],
            'TypeScript': [
                (r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', 'import'),
                (r'(?:function|const|let|var)\s+(\w+)\s*[=\(]', 'function'),
            ],
            'Java': [
                (r'import\s+([\w.]+)', 'import'),
                (r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(', 'function'),
            ],
            'C++': [
                (r'#include\s*[<"]([^>"]+)[>"]', 'include'),
                (r'(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{', 'function'),
            ],
            'C': [
                (r'#include\s*[<"]([^>"]+)[>"]', 'include'),
                (r'(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{', 'function'),
            ],
            'Go': [
                (r'import\s+\([^)]*[\'"]([^\'"]+)[\'"]', 'import'),
                (r'func\s+(\w+)', 'function'),
            ],
            'Rust': [
                (r'use\s+([\w:]+)', 'use'),
                (r'fn\s+(\w+)', 'function'),
            ],
            'C#': [
                (r'using\s+([\w.]+)', 'using'),
                (r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(', 'function'),
            ],
            'Ruby': [
                (r'require\s+[\'"]([^\'"]+)[\'"]', 'require'),
                (r'def\s+(\w+)', 'function'),
            ],
            'PHP': [
                (r'require|include.*?[\'"]([^\'"]+)[\'"]', 'require'),
                (r'function\s+(\w+)', 'function'),
            ],
            'Swift': [
                (r'import\s+(\w+)', 'import'),
                (r'func\s+(\w+)', 'function'),
            ],
            'Kotlin': [
                (r'import\s+([\w.]+)', 'import'),
                (r'fun\s+(\w+)', 'function'),
            ],
        }
        
        lang_patterns = patterns.get(language, [])
        
        for line_num, line in enumerate(source_lines, 1):
            for pattern, pattern_type in lang_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    if pattern_type in ['import', 'require', 'include', 'use', 'using']:
                        lib = match.group(1).split('/')[-1].split('.')[0]
                        if lib and not lib.startswith('.'):
                            libraries.add(lib)
                    elif pattern_type == 'function':
                        func_name = match.group(1)
                        if func_name and func_name not in ['if', 'for', 'while', 'switch', 'case']:
                            # Check if function already added
                            if not any(f[0] == func_name for f in functions):
                                # Extract function code (simplified - find next closing brace)
                                func_code = self._extract_function_code(source_lines, line_num - 1, language)
                                summary = f"Function: {func_name}"
                                functions.append((func_name, summary, func_code))
        
        return sorted(libraries), functions
    
    def _extract_function_code(self, source_lines: List[str], start_line: int, language: str) -> str:
        """Extract function code block"""
        if start_line >= len(source_lines):
            return ""
        
        # Simple extraction: get function line and next few lines
        end_line = min(start_line + 20, len(source_lines))
        return '\n'.join(source_lines[start_line:end_line])
    
    def build_generic_tree(self, source: str, language: str) -> List[Dict[str, Any]]:
        """Build generic code tree for non-Python languages"""
        structure = []
        source_lines = source.splitlines()
        
        # Extract classes and functions using regex
        class_patterns = {
            'Java': r'class\s+(\w+)',
            'C++': r'class\s+(\w+)',
            'C#': r'class\s+(\w+)',
            'JavaScript': r'class\s+(\w+)',
            'TypeScript': r'class\s+(\w+)',
        }
        
        func_patterns = {
            'JavaScript': r'(?:function|const|let|var)\s+(\w+)\s*[=\(]',
            'TypeScript': r'(?:function|const|let|var)\s+(\w+)\s*[=\(]',
            'Java': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(',
            'C++': r'(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{',
            'C': r'(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{',
            'Go': r'func\s+(\w+)',
            'Rust': r'fn\s+(\w+)',
            'C#': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(',
            'Ruby': r'def\s+(\w+)',
            'PHP': r'function\s+(\w+)',
            'Swift': r'func\s+(\w+)',
            'Kotlin': r'fun\s+(\w+)',
        }
        
        class_pattern = class_patterns.get(language)
        func_pattern = func_patterns.get(language)
        
        seen_classes = set()
        seen_functions = set()
        
        for line_num, line in enumerate(source_lines, 1):
            if class_pattern:
                class_match = re.search(class_pattern, line)
                if class_match:
                    class_name = class_match.group(1)
                    if class_name not in seen_classes:
                        seen_classes.add(class_name)
                        structure.append({
                            'type': 'class',
                            'name': class_name,
                            'parent': '',
                            'level': 0,
                            'args': []
                        })
            
            if func_pattern:
                func_match = re.search(func_pattern, line)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name not in ['if', 'for', 'while', 'switch', 'case'] and func_name not in seen_functions:
                        seen_functions.add(func_name)
                        structure.append({
                            'type': 'function',
                            'name': func_name,
                            'parent': '',
                            'level': 0,
                            'args': []
                        })
        
        return structure
    
    def analyze(self, code_text: str, filename: str) -> Dict:
        language = self.detect_language(filename, code_text)
        
        if language == 'Python':
            libraries, functions = self.parse_python(code_text)
            code_tree = self.build_code_tree(code_text)
            tree_graphviz = self.generate_tree_graphviz(code_tree=code_tree) if code_tree else None
        else:
            libraries, functions = self.parse_generic(code_text, language)
            code_tree = self.build_generic_tree(code_text, language)
            tree_graphviz = self.generate_tree_graphviz(code_tree=code_tree) if code_tree else None
        
        return {
            'language': language,
            'loc': self.count_loc(code_text),
            'libraries': libraries,
            'functions': functions,
            'code_tree': code_tree,
            'tree_graphviz': tree_graphviz
        }
