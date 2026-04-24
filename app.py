import streamlit as st
from tavily import TavilyClient
from google import genai

# =========================
# API KEYS
# =========================
TAVILY_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyCg1xZ9aCUJ4m6sxdHs58LTsym7w1mrSV8"

# =========================
# CLIENTS
# =========================
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

client = genai.Client(api_key=GEMINI_API_KEY)

# =========================
# UI
# =========================
st.set_page_config(page_title="Legal AI Agent")

st.title("⚖️ Legal Document Explainer")

uploaded_file = st.file_uploader("Upload txt file", type=["txt"])


def explain_text(text):
    try:
        # Tavily search
        response = tavily_client.search(query=text, search_depth="basic")
        results = response.get("results", [])[:3]

        raw = " ".join([r.get("content", "") for r in results])

        prompt = f"""
Explain this legal text in very simple English:

{raw}
"""

        # Gemini call (NEW SDK)
        result = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return result.text

    except Exception as e:
        return f"Error: {e}"


if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    st.write("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze"):
        st.write(explain_text(text))
