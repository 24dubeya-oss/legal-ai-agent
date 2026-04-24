import streamlit as st
from tavily import TavilyClient

# =========================
# 🔑 API KEY
# =========================
TAVILY_API_KEY = "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"

client = TavilyClient(api_key=TAVILY_API_KEY)

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Legal Document Explainer")

st.title("⚖️ Legal Document Explainer (Tavily AI Agent)")
st.write("Upload a legal document and get a simple explanation.")

uploaded_file = st.file_uploader("Upload your legal document", type=["txt"])


# =========================
# STEP 1: EXPLANATION ENGINE
# =========================
def explain_text(text):
    try:
        response = client.search(
            query=f"Explain this legal document in simple English: {text}",
            search_depth="basic"
        )

        results = response.get("results", [])[:3]

        if not results:
            return "No relevant information found."

        raw_text = " ".join([r.get("content", "") for r in results])

        cleaned = raw_text.replace("\n", " ").strip()

        return cleaned

    except Exception as e:
        return f"Error: {e}"


# =========================
# STEP 2: LLM-AS-A-JUDGE (RULE BASED)
# =========================
def llm_judge(text):
    score = 0

    # Rule 1: length check
    if len(text) > 50:
        score += 1

    # Rule 2: legal relevance check
    keywords = ["agreement", "contract", "party", "services", "payment", "liability"]
    if any(k in text.lower() for k in keywords):
        score += 1

    # Rule 3: readability check
    if "." in text or "," in text:
        score += 1

    # Final score output
    return f"📊 LLM-as-a-Judge Score: {score}/3"


# =========================
# STEP 3: MAIN FLOW
# =========================
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Document")
    st.write(text)

    if st.button("Analyze Document"):
        with st.spinner("Processing..."):

            # AI OUTPUT (TAVILY)
            explanation = explain_text(text)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation)

        # JUDGE OUTPUT
        st.subheader("📊 Evaluation (LLM-as-a-Judge)")
        st.write(llm_judge(explanation))
