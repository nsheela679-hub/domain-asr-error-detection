import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

# ======================================================
# Helper Functions
# ======================================================

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def phrase_exists(phrase, text, threshold=0.65):
    """
    Checks if a domain phrase exists in text using:
    1. Direct substring match
    2. Sliding window fuzzy match
    """
    phrase = phrase.lower().strip()
    text = text.lower()

    if phrase in text:
        return True

    phrase_len = len(phrase.split())
    words = text.split()

    for i in range(len(words) - phrase_len + 1):
        window = " ".join(words[i:i + phrase_len])
        if similarity(phrase, window) >= threshold:
            return True

    return False


# ======================================================
# Streamlit UI
# ======================================================

st.set_page_config(
    page_title="Domain ASR Error Detection",
    layout="wide"
)

st.title("🧠 Domain-Specific ASR Error Detection")
st.write(
    "Detect **missing or mis-recognized domain terms** by comparing "
    "ASR output with corrected transcripts."
)

# ======================================================
# File Upload
# ======================================================

asr_file = st.file_uploader("Upload ASR Transcript (Excel)", type=["xlsx"])
corrected_file = st.file_uploader("Upload Corrected Transcript (Excel)", type=["xlsx"])
domain_file = st.file_uploader("Upload Domain Dictionary (Excel)", type=["xlsx"])

# ======================================================
# Processing Logic
# ======================================================

if asr_file and corrected_file and domain_file:

    asr_df = pd.read_excel(asr_file)
    corr_df = pd.read_excel(corrected_file)
    domain_df = pd.read_excel(domain_file)

    domain_terms = (
        domain_df.iloc[:, 0]
        .astype(str)
        .str.lower()
        .str.strip()
        .dropna()
        .unique()
    )

    errors = []

    total_rows = min(len(asr_df), len(corr_df))

    for i in range(total_rows):

        asr_text = str(asr_df.iloc[i, 0])
        corr_text = str(corr_df.iloc[i, 0])

        missing_terms = []

        for term in domain_terms:
            # Term exists in corrected but missing in ASR
            if phrase_exists(term, corr_text) and not phrase_exists(term, asr_text):
                missing_terms.append(term)

        if missing_terms:
            errors.append({
                "Row_No": i + 1,
                "Corrected_Text": corr_text,
                "ASR_Text": asr_text,
                "Missing_Domain_Terms": ", ".join(missing_terms)
            })

    # ======================================================
    # Output
    # ======================================================

    st.subheader("📌 Detected Domain Errors")

    if errors:
        error_df = pd.DataFrame(errors)
        st.dataframe(error_df, use_container_width=True)
        st.success(f"✅ {len(error_df)} rows with domain ASR errors detected")
    else:
        st.warning("❌ No domain-specific ASR errors found")

else:
    st.info("⬆️ Please upload **all three Excel files** to continue")
