# DCPify 🚀

DCPify is a local-first Python tool that automatically detects computationally expensive functions in your codebase and refactors them into **DCP-compatible** (Distributive Compute Platform) workloads using the Gemini API.

It bridges the gap between local development and distributed computing by automating the "DCP-ification" of your heavy workloads.

## Key Features
- **Static Code Scanning**: Uses AST analysis to identify loops and operations involving heavy libraries (numpy, scipy, etc.).
- **AI-Powered Refactoring**: Leverages Gemini 2.0 to rewrite local functions into pure, side-effect-free DCP work functions.
- **Integrated Orchestration**: Generates a complete, ready-to-run DCP project under `output/dcp/` with a synchronous orchestrator script.
- **Convention Driven**: Follows official DCP Python patterns, including `dcp.progress()` reporting and integrated dependency handling.

## Prerequisites
1. **DCP Identity**: You need the following keystore files in your `~/.dcp/` directory:
   - `id.keystore` (Primary identity)
   - `default.keystore` (Default compute group account)
   - Register at [DCP Portal](https://portal.dcp.live) to export these.
2. **Node.js**: Required for the DCP runtime.
3. **DCP Packages**:
   - For Python jobs: `pip install dcp-client` or `pip install dcp`
   - For Node.js jobs: `npm i dcp-client`
4. **Gemini API Key**: Get a key from [Google AI Studio](https://aistudio.google.com/).
5. **Python 3.10+**

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd dcpify

# Install dependencies
pip install dcp-client
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Usage
Run the generator against any Python project directory or file:
```bash
python3 dcpify.py /path/to/your/project
```

### 4. Run the DCP Job
Once the process completes, navigate to the output and run the integrated orchestrator:
```bash
cd output/dcp
python3 job.py
```

## Project Structure
- `dcpify.py`: CLI entry point and orchestration logic.
- `scan.py`: Codebase scanner using static analysis.
- `gemini.py`: Gemini API integration with SSL and rate-limit handling.
- `templates/`:
  - `prompt.txt`: AI instructions for refactoring.
  - `orchestrator.py`: Template for the final job script.
- `output/dcp/`: Generated work functions and integrated job script.

## How it works
1. **Scans** the target path for functions with a "complexity score" > 5.
2. **Refactors** functions via Gemini into self-contained units (no global state, local imports).
3. **Extracts** required Pip modules from the AI's output.
4. **Assembles** the refactored functions and configuration into `job.py`.

## Important Notes
- **SSL Verification**: The tool includes a workaround for environment-specific SSL certificate issues.
- **Rate Limits**: Includes a 1s delay between API calls to accommodate Gemini free-tier quotas.
- **Manual Verification**: Always review generated code in `output/dcp/work/` before execution.
# dcpify
