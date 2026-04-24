import streamlit as st
from tavily import TavilyClient

# 🔑 Put your Tavily API key here
TAVILY_API_KEY = "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"

client = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer")
st.write("Upload a legal document and get a simple explanation.")

# 📂 File upload
uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])

def explain_text(text):
    response = client.search(query=text, search_depth="basic")

    results = response["results"][:3]

    raw_text = " ".join([r["content"] for r in results])

    # SIMPLE CLEANING (removes junk feel)
    cleaned = raw_text.split("Page")[0].split("ATTORNEY")[0]

    return "🧠 Simple Explanation:\n\n" + cleaned

# 🚀 Analyze button
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Processing..."):
            explanation = explain_text(text)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation)
