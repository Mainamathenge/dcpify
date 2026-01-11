import os
import sys
import argparse
import shutil
from scan import scan_codebase
from gemini import call_gemini

# Paths
OUTPUT_DIR = os.path.join("output", "dcp")
WORK_DIR = os.path.join(OUTPUT_DIR, "work")
TEMPLATES_DIR = "templates"
PROMPT_FILE = os.path.join(TEMPLATES_DIR, "prompt.txt")
ORCHESTRATOR_TEMPLATE = os.path.join(TEMPLATES_DIR, "orchestrator.py")
OUTPUT_JOB_FILE = os.path.join(OUTPUT_DIR, "job.py")

DCP_SETUP_INSTRUCTIONS = """
[!] DCP Identity Missing!
==================================================
To run distributed jobs, you must have a DCP Identity.

1. GET KEYSTORES: Log in to the DCP Portal and export your 'id.keystore' and 'default.keystore'.
2. PLACEMENT:    Move them to: ~/.dcp/
3. PERMISSIONS:  Ensure secure permissions:
                 chmod 600 ~/.dcp/*.keystore
4. INSTALL:      pip install dcp-client
                 npm i dcp-client (if using node components)

The tool will exit now until the keystores are configured.
==================================================
"""

def check_dcp_setup():
    """Verify that the DCP environment is configured."""
    keystore_path = os.path.expanduser("~/.dcp/id.keystore")
    if not os.path.exists(keystore_path):
        print(DCP_SETUP_INSTRUCTIONS.format(keystore_path=keystore_path))
        sys.exit(1)
    print(f"[*] DCP Identity verified at: {keystore_path}")

def setup_environment():
    """Ensure the output directory structure exists."""
    os.makedirs(WORK_DIR, exist_ok=True)
    print(f"[*] Output directory ready: {WORK_DIR}")

def load_prompt_template():
    """Load the prompt template from the templates directory."""
    if not os.path.exists(PROMPT_FILE):
        print(f"[!] Error: Prompt template not found at {PROMPT_FILE}")
        sys.exit(1)
    with open(PROMPT_FILE, "r") as f:
        return f.read()

def clean_llm_output(text):
    """Remove markdown formatting and extract modules tag."""
    text = text.strip()
    if text.startswith("```python"):
        text = text[9:]
    if text.endswith("```"):
        text = text[:-3]
    
    lines = text.splitlines()
    modules = []
    clean_lines = []
    
    for line in lines:
        if "# MODULES:" in line:
            parts = line.split("# MODULES:", 1)[1].strip().split(",")
            modules = [p.strip() for p in parts if p.strip() and p.strip().lower() != "none"]
        else:
            clean_lines.append(line)
            
    return "\n".join(clean_lines).strip(), modules

def generate_orchestrator(candidates, rewritten_codes, all_modules):
    """Create a job.py by injecting generated code into the template."""
    if not os.path.exists(ORCHESTRATOR_TEMPLATE):
        print(f"[!] Warning: Orchestrator template not found at {ORCHESTRATOR_TEMPLATE}")
        return

    with open(ORCHESTRATOR_TEMPLATE, "r") as f:
        template = f.read()

    # For simplicity, we use the first candidate as the primary job name 
    # and combine all rewritten functions into the script.
    primary_cand = candidates[0]
    combined_code = "\n\n".join(rewritten_codes)
    unique_modules = sorted(list(set(all_modules)))

    # Basic input set placeholder - in a real app this would be more dynamic
    input_set = "[1, 2, 3, 4, 5] # TODO: Replace with real data"

    output = template.replace("{{FUNCTION_CODE}}", combined_code)
    output = output.replace("{{FUNCTION_NAME}}", primary_cand['name'])
    output = output.replace("{{INPUT_SET}}", input_set)
    output = output.replace("{{MODULES}}", str(unique_modules))
    output = output.replace("{{JOB_NAME}}", f"DCPify: {primary_cand['name']}")

    with open(OUTPUT_JOB_FILE, "w") as f:
        f.write(output)
        
    print(f"[*] Generated integrated orchestrator: {OUTPUT_JOB_FILE}")

def main():
    check_dcp_setup()
    
    # 1. Get Target Directory Interactively
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        print("\n--- DCPify Startup ---")
        target_path = input("Enter the path to the Python project you want to scan: ").strip()
    
    if not target_path or not os.path.exists(target_path):
        print(f"[!] Invalid path: {target_path}")
        return

    setup_environment()
    prompt_template = load_prompt_template()

    print(f"\n[*] Scanning codebase: {os.path.abspath(target_path)}")
    candidates = scan_codebase(target_path)

    if not candidates:
        print("[!] No expensive functions found (Score < 5).")
        return

    # 2. Display Expensive Functions Found
    print(f"\n[*] Found {len(candidates)} computationally expensive function(s):")
    print("-" * 60)
    for i, cand in enumerate(candidates, 1):
        print(f"{i}. {cand['name']} | Score: {cand['score']} | File: {cand['file']}")
    print("-" * 60)

    rewritten_codes = []
    all_modules = []

    for cand in candidates:
        name = cand['name']
        code = cand['code']

        print(f"\n[>] Processing: {name}...")
        
        # Prepare prompt
        prompt = prompt_template.format(code=code)
        
        print(f"    - Sending to Gemini for refactoring...")
        try:
            raw_output = call_gemini(prompt)
            rewritten_code, modules = clean_llm_output(raw_output)
            
            rewritten_codes.append(rewritten_code)
            all_modules.extend(modules)
            
            output_path = os.path.join(WORK_DIR, f"{name}.py")
            with open(output_path, "w") as f:
                f.write(rewritten_code)
            
            print(f"    - [OK] Saved work function to: {output_path}")
            if modules:
                print(f"    - [INFO] Required modules: {', '.join(modules)}")
        except Exception as e:
            print(f"    - [ERROR] Failed to process {name}: {e}")
        
        import time
        time.sleep(1) # Respect free tier rate limits

    if rewritten_codes:
        generate_orchestrator(candidates, rewritten_codes, all_modules)

    # 3. Final Summary with Absolute Paths
    abs_output_dir = os.path.abspath(OUTPUT_DIR)
    
    print("\n" + "="*60)
    print("DCPify Process Complete")
    print("="*60)
    print(f"[*] DCP-ready project path: {abs_output_dir}")
    print(f"[*] Work functions: {os.path.join(abs_output_dir, 'work')}")
    print(f"[*] Orchestrator:    {os.path.join(abs_output_dir, 'job.py')}")
    print("\nNext Steps:")
    print(f" 1. Review the generated code in {os.path.join(abs_output_dir, 'work')}")
    print(f" 2. Ensure your id.keystore is ready.")
    print(f" 3. Run: python3 {os.path.join(abs_output_dir, 'job.py')}")

if __name__ == "__main__":
    main()
