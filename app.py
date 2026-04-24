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
    try:
        response = client.search(
            query=text,
            search_depth="basic"
        )

        # Take top 3 results
        results = response["results"][:3]

        # Combine content properly
        combined_text = " ".join([r["content"] for r in results])

        return "🧠 Simple Explanation:\n\n" + combined_text

    except Exception as e:
        return f"Error: {e}"

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
