import ast
import os

EXPENSIVE_MODULES = {'numpy', 'pandas', 'torch', 'cv2', 'scipy', 'np', 'pd', 'cv'}
EXPENSIVE_FUNCTIONS = {'dot', 'matmul', 'random', 'exp', 'sqrt', 'mean', 'std', 'sum', 'max', 'min', 'zeros', 'ones', 'array', 'linspace', 'arange'}

class ComputeScoreVisitor(ast.NodeVisitor):
    def __init__(self):
        self.score = 0
        self.has_expensive_import = False
        self.loop_depth = 0

    def visit_For(self, node):
        # Nested loops get exponentially higher scores
        self.loop_depth += 1
        self.score += 2 * self.loop_depth
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        # Nested loops get exponentially higher scores
        self.loop_depth += 1
        self.score += 2 * self.loop_depth
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Call(self, node):
        # Check if it's a numpy/scipy function call
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in EXPENSIVE_MODULES:
                self.score += 2
            elif node.func.attr in EXPENSIVE_FUNCTIONS:
                self.score += 1
        self.score += 1
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Heuristic: check for usage of likely expensive libraries like np.dot, cv2.resize
        if isinstance(node.value, ast.Name) and node.value.id in EXPENSIVE_MODULES:
            self.score += 1
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

    # Iterate over top-level nodes in the module
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            visitor = ComputeScoreVisitor()
            visitor.visit(node)
            
            # Debug: print all functions and their scores
            print(f"  Function '{node.name}': score = {visitor.score}")
            
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
    
    # Handle both file and directory inputs
    if os.path.isfile(root_dir):
        # Single file
        if root_dir.endswith('.py'):
            print(f"Analyzing file: {root_dir}")
            candidates.extend(analyze_file(root_dir))
    else:
        # Directory
        for root, dirs, files in os.walk(root_dir):
            # Skip hidden folders and our own output
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'output']
            
            for file in files:
                if file.endswith('.py') and file != 'scan.py' and file != 'gemini.py' and file != 'dcpify.py':
                     filepath = os.path.join(root, file)
                     print(f"Analyzing file: {filepath}")
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
