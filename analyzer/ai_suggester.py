import json
import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()  # Load environment variables from .env file

# Model can be overridden via the GEMINI_MODEL env var.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

_client = None


def _get_client():
    """
    Lazily create and return the Gemini client.

    The API key is read on first use rather than at import time, so the module
    can be imported (e.g. by the test suite) without a key being present.
    """
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )
        _client = genai.Client(api_key=api_key)
    return _client


# NOTE: The function name and output keys are kept as `analyze_with_gpt4` / "gpt4"
# for backward compatibility with the rest of the pipeline (run_analysis.py, app.py,
# and the outputs/gpt4_main_tf.json artifact). Only the underlying model has changed
# to Google Gemini.
def analyze_with_gpt4(file_path: str) -> list:
    """
    Analyzes a Terraform file using Google Gemini and returns a structured issue list.
    Returns a list of dicts: [{"type": ..., "line": ..., "message": ...}]
    """
    try:
        with open(file_path, "r") as f:
            code = f.read()

        prompt = f"""
You are an AI cloud infrastructure auditor. Analyze the following Terraform code and return a JSON array of issues found.

For each issue, include:
- "type": one of ["Security Risk", "Best Practice", "Warning"]
- "line": line number (approximate is OK)
- "message": brief explanation

Respond ONLY with a JSON array. No extra commentary.

Terraform Code:
```hcl
{code}
```"""

        response = _get_client().models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2),
        )

        reply = response.text.strip()

        # Gemini sometimes wraps JSON in markdown code fences; strip them if present.
        if reply.startswith("```"):
            reply = re.sub(r"^```(?:json)?\s*", "", reply)
            reply = re.sub(r"\s*```$", "", reply)

        issues = json.loads(reply.strip())
        return issues

    except Exception as e:
        print(f"[❌] Gemini analysis failed: {e}")
        return []
