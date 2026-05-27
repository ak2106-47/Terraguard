import streamlit as st
import json
import matplotlib.pyplot as plt
from collections import Counter
import re

# --- SETUP ---
st.set_page_config(page_title="TerraGuard", page_icon="☁️", layout="wide")

# --- LOGO & HEADER ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("assets/terraguard_logo.png", width=300)
st.title("TerraGuard")
st.subheader("Your AI Mentor for Infrastructure-as-Code")


# --- SIDEBAR AI Q&A ---
with st.sidebar:
    st.header("🧠 Ask TerraGuard")
    user_q = st.text_input("Ask a question about the issues:")

    def extract_top_issue(data):
        issues = data.get("issues_detected") or data.get("issues", [])
        risks = [i for i in issues if i.get("type", "").lower() == "security risk"]
        return risks[0] if risks else (issues[0] if issues else None)

    if user_q:
        try:
            with open("outputs/gpt4_main_tf.json", "r", encoding="utf-8") as f:
                gpt_data = json.load(f)
            top_issue = extract_top_issue(gpt_data)
            if top_issue and "biggest" in user_q.lower() and "risk" in user_q.lower():
                st.success(f"⚠️ {top_issue['type']} at line {top_issue['line']}: {top_issue['message']}")
            else:
                st.info("🔍 Try asking: 'What is the biggest risk in this file?'")
        except Exception as e:
            st.error(f"❌ Could not load Gemini analysis data.\n{str(e)}")

# --- FILE SELECTION ---
option = st.selectbox("Choose a model output to view:", ("Gemini", "CodeBERT", "Comparison Report"))

# --- DISPLAY JSON ---
if option == "Gemini":
    with open("outputs/gpt4_main_tf.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    st.json(data)

elif option == "CodeBERT":
    with open("outputs/codebert_main_tf.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    st.json(data)

# --- MARKDOWN REPORT WITH TABS ---
elif option == "Comparison Report":
    with open("outputs/comparison_report.md", "r", encoding="utf-8") as f:
        md = f.read()

    summary = re.search(r"## Summary\n(.*?)\n##", md, re.DOTALL)
    summary = summary.group(1) if summary else "No summary found."

    insights = re.search(r"## Key Insights\n(.*?)\n##", md, re.DOTALL)
    insights = insights.group(1) if insights else "No insights found."

    recommendations = re.search(r"## Recommendations\n(.*)", md, re.DOTALL)
    recommendations = recommendations.group(1) if recommendations else "No recommendations found."

    tab1, tab2, tab3 = st.tabs(["📝 Summary", "📌 Key Insights", "✅ Recommendations"])
    with tab1:
        st.markdown(summary)
    with tab2:
        st.markdown(insights)
    with tab3:
        st.markdown(recommendations)

# --- ISSUE BAR CHART ---
st.markdown("---")
st.header("📊 Gemini vs CodeBERT Issue Comparison")

def count_issues(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    issues = data.get("issues_detected") or data.get("issues", [])
    return Counter(issue.get("type", "Unknown") for issue in issues)

gpt4_counts = count_issues("outputs/gpt4_main_tf.json")
codebert_counts = count_issues("outputs/codebert_main_tf.json")
all_types = sorted(set(gpt4_counts) | set(codebert_counts))
gpt4_data = [gpt4_counts.get(t, 0) for t in all_types]
codebert_data = [codebert_counts.get(t, 0) for t in all_types]

fig, ax = plt.subplots(figsize=(5, 3))
bar_width = 0.35
x = range(len(all_types))

ax.bar([i - bar_width/2 for i in x], gpt4_data, width=bar_width, label='Gemini', color='skyblue')
ax.bar([i + bar_width/2 for i in x], codebert_data, width=bar_width, label='CodeBERT', color='salmon')

ax.set_xlabel('Issue Type')
ax.set_ylabel('Count')
ax.set_title('Issue Type Comparison')
ax.set_xticks(list(x))
ax.set_xticklabels(all_types)
ax.legend()
st.pyplot(fig)

# --- FILE UPLOAD FOR LIVE ANALYSIS ---
st.markdown("---")
st.header("📂 Upload a Terraform File for Live Analysis")

uploaded_file = st.file_uploader("Upload a .tf file", type=["tf"])
if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.code(code, language="hcl")

    # Very basic inline rule engine logic (for demo)
    if "public-read" in code:
        st.error("❌ Security Risk: Found 'public-read' ACL — may expose data.")
    if "ami-" in code:
        st.warning("⚠️ Best Practice: Hardcoded AMI ID found. Consider using a variable.")
    if "t2.micro" in code:
        st.warning("⚠️ Best Practice: Hardcoded instance type 't2.micro'.")
