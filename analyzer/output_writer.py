import json
import os
from datetime import datetime

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_json_output(model_name: str, filename: str, issues: list, metadata: dict = None):
    """
    Writes analysis results to a JSON file.

    Parameters:
    - model_name (str): Name of the AI model (e.g., 'gpt4', 'codebert').
    - filename (str): Name of the IaC file analyzed.
    - issues (list): List of issues or suggestions (dicts with 'type', 'line', 'message').
    - metadata (dict): Optional metadata (timestamp, file size, etc.)
    """
    output = {
        "model": model_name,
        "file_analyzed": filename,
        "issues_detected": issues,
        "metadata": metadata or {},
        "timestamp": datetime.now().isoformat()
    }

    outfile = os.path.join(OUTPUT_DIR, f"{model_name}_{filename.replace('.','_')}.json")
    with open(outfile, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[✅] Output written to {outfile}")
    return outfile


def write_markdown_report(model_outputs: list, output_file="comparison_report.md"):
    """
    Writes a Markdown comparison report of model outputs.

    Parameters:
    - model_outputs (list): List of dictionaries from write_json_output, each with model, issues, etc.
    - output_file (str): Markdown file name.
    """
    lines = ["# TerraGuard AI Model Comparison Report\n"]

    for result in model_outputs:
        lines.append(f"## Model: {result['model']}")
        lines.append(f"**File Analyzed:** `{result['file_analyzed']}`")
        lines.append(f"**Issues Detected:** {len(result['issues_detected'])}")
        lines.append("")

        for issue in result["issues_detected"]:
            lines.append(f"- 🔍 **{issue['type']}** at line {issue['line']}: {issue['message']}")

        lines.append("\n---\n")

    outfile = os.path.join(OUTPUT_DIR, output_file)
    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[📄] Markdown report saved to {outfile}")
    return outfile
