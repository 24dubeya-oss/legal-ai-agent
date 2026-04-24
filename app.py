import streamlit as st
import requests
from tavily import TavilyClient

# 🔑 Add your Tavily key here
TAVILY_API_KEY = "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"

tavily = TavilyClient(api_key=TAVILY_API_KEY)

# 🧠 Ollama call
def ollama_call(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",  # or "phi"
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# 📄 Explain
def explain_text(text):
    prompt = f"""
Explain this legal document in VERY SIMPLE ENGLISH.
Use short sentences. Only English.

{text}
"""
    return ollama_call(prompt)

# 📝 Summary
def summarize_text(text):
    prompt = f"""
Give a SHORT SUMMARY of this legal document in 3-4 lines.

{text}
"""
    return ollama_call(prompt)

# ⚠️ Risk Detection
def detect_risk(text):
    prompt = f"""
Find any RISKS or dangerous clauses in this legal document.
Explain in simple points.

{text}
"""
    return ollama_call(prompt)

# 🧪 LLM-as-Judge
def judge_output(explanation):
    prompt = f"""
Rate this explanation from 1 to 10 based on clarity and simplicity.
Also give a short reason.

Explanation:
{explanation}
"""
    return ollama_call(prompt)

# 🔎 Tavily Search
def search_info(query):
    result = tavily.search(query=query)
    return str(result)

# 🌐 UI
st.set_page_config(page_title="Legal AI Agent", page_icon="📄")

st.title("📄 Legal Document Explainer AI (Agentic)")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Original Text")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Processing..."):

            explanation = explain_text(text)
            summary = summarize_text(text)
            risks = detect_risk(text)
            score = judge_output(explanation)
            extra = search_info("legal agreement meaning")

        st.subheader("🧠 Explanation")
        st.write(explanation)

        st.subheader("📝 Summary")
        st.write(summary)

        st.subheader("⚠️ Risks")
        st.write(risks)

        st.subheader("🧪 AI Judge Score")
        st.write(score)

        st.subheader("🔎 Extra Info (Tavily)")
        st.write(extra)