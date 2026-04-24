import streamlit as st
from tavily import TavilyClient

# =========================
# API KEY
# =========================
TAVILY_API_KEY = "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"

client = TavilyClient(api_key=TAVILY_API_KEY)

# =========================
# UI
# =========================
st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer (No Gemini Version)")

uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])


def explain_text(text):
    try:
        response = client.search(query=text, search_depth="basic")

        results = response.get("results", [])[:3]

        if not results:
            return "No relevant information found."

        raw = " ".join([r.get("content", "") for r in results])

        # SIMPLE CLEAN SUMMARY (no AI model)
        summary_prompt = f"""
Simplify this legal text into easy English:

{raw}
"""

        return summary_prompt

    except Exception as e:
        return f"Error: {e}"


if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    st.write("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze"):
        st.subheader("🧠 Simple Explanation")
        st.write(explain_text(text))
