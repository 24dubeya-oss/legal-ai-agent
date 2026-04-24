import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# =========================
# 🔑 API KEYS
# =========================
TAVILY_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyC8vcn9a01-_3rLL3Rm7vHD8ZXqhkWBAiM"  

# =========================
# INIT CLIENTS
# =========================
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)

# ✅ SAFE MODEL (most compatible across accounts)
model = genai.GenerativeModel("gemini-pro")


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer")
st.write("Upload a legal document and get a simple explanation.")


uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])


# =========================
# AI FUNCTION
# =========================
def explain_text(text):
    try:
        # STEP 1: Tavily search
        response = tavily_client.search(
            query=text,
            search_depth="basic"
        )

        results = response.get("results", [])[:3]

        if not results:
            return "No relevant information found."

        raw_text = " ".join([r.get("content", "") for r in results])

        # STEP 2: Gemini explanation
        prompt = f"""
You are a legal assistant AI.

Explain this legal document in very simple English.

Rules:
- Use simple language
- Do NOT copy legal text
- Keep it short and clear
- Use bullet points if needed

TEXT:
{raw_text}
"""

        result = model.generate_content(prompt)

        return result.text if result.text else "No response from AI."

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# MAIN APP FLOW
# =========================
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Processing..."):
            explanation = explain_text(text)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation)
