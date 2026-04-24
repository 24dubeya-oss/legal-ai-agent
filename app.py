import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# 🔑 API KEYS (IMPORTANT: move to Railway Variables later)
TAVILY_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyDJPQxaSBc2mjKpMYgxAm3YtEvsnOQbJ6E" 

# Initialize clients
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Correct working model
model = genai.GenerativeModel("gemini-pro")

# UI setup
st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer")
st.write("Upload a legal document and get a simple explanation.")

# File upload
uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])


def explain_text(text):
    try:
        # Step 1: Tavily search
        response = tavily_client.search(
            query=text,
            search_depth="basic"
        )

        results = response["results"][:3]
        raw_text = " ".join([r["content"] for r in results])

        # Step 2: Gemini summarization
        prompt = f"""
You are a legal assistant AI.

Explain the following legal text in very simple English.
Make it easy for a student to understand.

Rules:
- Do NOT copy legal text
- Use simple language
- Use bullet points if needed

Text:
{raw_text}
"""

        result = model.generate_content(prompt)

        return result.text

    except Exception as e:
        return f"Error: {e}"


# Main app logic
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Processing..."):
            explanation = explain_text(text)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation)
