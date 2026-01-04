import ast
import os

EXPENSIVE_MODULES = {'numpy', 'pandas', 'torch', 'cv2', 'scipy', 'np', 'pd', 'cv'}

class ComputeScoreVisitor(ast.NodeVisitor):
    def __init__(self):
        self.score = 0
        self.has_expensive_import = False

    def visit_For(self, node):
        self.score += 2
        self.generic_visit(node)

    def visit_While(self, node):
        self.score += 2
        self.generic_visit(node)

    def visit_Call(self, node):
        self.score += 1
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Heuristic: check for usage of likely expensive libraries like np.dot, cv2.resize
        if isinstance(node.value, ast.Name) and node.value.id in EXPENSIVE_MODULES:
            self.score += 2
        self.generic_visit(node)

def get_function_source(lines, node):
    """
    Extracts the function source code from the list of lines 
    using the node's lineno and end_lineno.
    """
    if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
        return ""
    
    # helper for 1-based indexing
    start_index = node.lineno - 1
    end_index = node.end_lineno
    
    return "".join(lines[start_index:end_index])

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            source = f.read()
            tree = ast.parse(source)
            source_lines = source.splitlines(keepends=True)
        except Exception as e:
            print(f"Skipping {filepath} due to parse error: {e}")
            return []

    results = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            visitor = ComputeScoreVisitor()
            visitor.visit(node)
            
            if visitor.score >= 5:
                # Extract source code for the function
                func_source = get_function_source(source_lines, node)
                results.append({
                    'name': node.name,
                    'file': filepath,
                    'score': visitor.score,
                    'code': func_source
                })

    return results

def scan_codebase(root_dir):
    candidates = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden folders and our own output
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'output']
        
        for file in files:
            if file.endswith('.py') and file != 'scan.py' and file != 'gemini.py' and file != 'dcpify.py':
                 filepath = os.path.join(root, file)
                 candidates.extend(analyze_file(filepath))
    
    return candidates

if __name__ == "__main__":
    # Test run
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    results = scan_codebase(target)
    print(f"Found {len(results)} candidates:")
    for res in results:
        print(f"- {res['name']} ({res['file']}) | Score: {res['score']}")
