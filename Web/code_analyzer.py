import ast
from typing import Dict, List, Tuple, Any


class CodeAnalyzer:
    def detect_language(self, filename: str) -> str:
        return "Python" if filename.endswith(".py") else "Unknown"
    
    def count_loc(self, text: str) -> int:
        return sum(1 for line in text.splitlines() if line.strip())
    
    def parse_python(self, source: str) -> Tuple[List[str], List[Tuple[str, str]]]:
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
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)
                if doc:
                    summary = doc.strip().split("\n")[0]
                else:
                    arg_names = [a.arg for a in node.args.args]
                    summary = f"Function with parameters: {', '.join(arg_names)}" if arg_names else "Function with no parameters"
                functions.append((node.name, summary))
        
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
    
    def generate_tree_graphviz(self, source: str) -> str:
        """Generate Graphviz DOT format for code tree"""
        tree = self.build_code_tree(source)
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
    
    def analyze(self, code_text: str, filename: str) -> Dict:
        libraries, functions = self.parse_python(code_text)
        code_tree = self.build_code_tree(code_text)
        tree_graphviz = self.generate_tree_graphviz(code_text)
        return {
            'language': self.detect_language(filename),
            'loc': self.count_loc(code_text),
            'libraries': libraries,
            'functions': functions,
            'code_tree': code_tree,
            'tree_graphviz': tree_graphviz
        }
