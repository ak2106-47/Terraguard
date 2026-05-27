# run_analysis.py

import os
from analyzer.ai_suggester import analyze_with_gpt4
from analyzer.codebert_analyzer import CodeBERTAnalyzer
from analyzer.output_writer import (
    write_json_output,
    write_markdown_report,
)

# --- Config ---
TERRAFORM_FILE = "examples/main.tf"
MODEL_OUTPUTS = []

# --- Validate Terraform File ---
if not os.path.isfile(TERRAFORM_FILE):
    print(f"❌ Error: Terraform file '{TERRAFORM_FILE}' not found.")
    exit(1)

# --- Read Terraform Code ---
with open(TERRAFORM_FILE, "r") as f:
    terraform_code = f.read()

# --- Gemini Analysis ---
print("\n🔍 Running Gemini Analysis...\n")
gpt4_issues = analyze_with_gpt4(TERRAFORM_FILE)
gpt4_metadata = {
    "source": "Google Gemini",
    "num_issues": len(gpt4_issues)
}
gpt4_json = write_json_output("gpt4", os.path.basename(TERRAFORM_FILE), gpt4_issues, gpt4_metadata)
MODEL_OUTPUTS.append({
    "model": "Gemini",
    "file_analyzed": os.path.basename(TERRAFORM_FILE),
    "issues_detected": gpt4_issues
})

# --- CodeBERT Analysis ---
print("\n🤖 Running CodeBERT Analysis...\n")
codebert = CodeBERTAnalyzer()
label = codebert.analyze(terraform_code)

# Since CodeBERT currently outputs only 1 label for the whole file:
codebert_issues = [{
    "type": label,
    "line": "N/A",
    "message": f"CodeBERT classified the file as '{label}'"
}]
codebert_metadata = {
    "source": "Microsoft CodeBERT",
    "num_issues": 1
}
codebert_json = write_json_output("codebert", os.path.basename(TERRAFORM_FILE), codebert_issues, codebert_metadata)
MODEL_OUTPUTS.append({
    "model": "CodeBERT",
    "file_analyzed": os.path.basename(TERRAFORM_FILE),
    "issues_detected": codebert_issues
})

# --- Write Combined Markdown Report ---
write_markdown_report(MODEL_OUTPUTS)
