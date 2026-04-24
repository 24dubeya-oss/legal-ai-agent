import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# =========================
# 🔑 API KEYS (IMPORTANT)
# =========================
TAVILY_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyDJPQxaSBc2mjKpMYgxAm3YtEvsnOQbJ6E" 

# =========================
# CLIENT SETUP
# =========================
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)

# ✅ MOST STABLE MODEL (CURRENTLY WORKING WIDELY)
model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer")
st.write("Upload a legal document and get a simple explanation.")

uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])


# =========================
# AI FUNCTION (CORE LOGIC)
# =========================
def explain_text(text):
    try:
        # STEP 1: GET CONTEXT FROM TAVILY
        response = tavily_client.search(
            query=text,
            search_depth="basic"
        )

        results = response.get("results", [])[:3]

        # safety check (IMPORTANT)
        if not results:
            return "No relevant information found."

        raw_context = " ".join([r.get("content", "") for r in results])

        # STEP 2: SEND TO GEMINI FOR CLEAN EXPLANATION
        prompt = f"""
You are a legal assistant AI.

Task: Explain the given legal text in VERY SIMPLE English.

Rules:
- Use easy language
- Do NOT copy legal text
- Keep it short and clear
- Use bullet points if needed

Legal Text:
{raw_context}
"""

        result = model.generate_content(prompt)

        # safety check
        if result and result.text:
            return result.text
        else:
            return "AI did not return a valid response."

    except Exception as e:
        return f"Error occurred: {str(e)}"


# =========================
# APP FLOW
# =========================
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Analyzing with AI..."):
            explanation = explain_text(text)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation)
