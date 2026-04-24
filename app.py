import streamlit as st
from tavily import TavilyClient
from google import genai

# =========================
# 🔑 API KEYS
# =========================
TAVILY_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyDJPQxaSBc2mjKpMYgxAm3YtEvsnOQbJ6E" 

# =========================
# CLIENT SETUP
# =========================
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

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

        raw_context = " ".join([r.get("content", "") for r in results])

        # STEP 2: Gemini explanation (NEW SDK FIX)
        prompt = f"""
You are a legal assistant AI.

Explain the following legal text in very simple English.

Rules:
- Use simple words
- Do NOT copy legal text
- Make it short and clear
- Use bullet points if needed

Legal Text:
{raw_context}
"""

        response = gemini_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# APP LOGIC
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
