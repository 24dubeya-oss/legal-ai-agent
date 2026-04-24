import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# 🔑 API KEYS
TAVILY_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyDJPQxaSBc2mjKpMYgxAm3YtEvsnOQbJ6E" 

# Clients
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# UI
st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer")
st.write("Upload a legal document and get a simple explanation.")

uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])


def explain_text(text):
    try:
        # STEP 1: Get data from Tavily
        response = tavily_client.search(
            query=text,
            search_depth="basic"
        )

        results = response["results"][:3]
        raw_text = " ".join([r["content"] for r in results])

        # STEP 2: Send to Gemini for proper explanation
        prompt = f"""
You are a legal assistant AI.
Explain the following legal content in very simple English for a student.

Rules:
- Use simple words
- Do NOT copy legal text
- Give clear explanation in points if needed

Text:
{raw_text}
"""

        result = model.generate_content(prompt)

        return result.text

    except Exception as e:
        return f"Error: {e}"


# UI logic
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Processing..."):
            explanation = explain_text(text)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation)
