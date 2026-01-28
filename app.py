import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

# ---------- Helper functions ----------
def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def exists_similar(word, word_list, threshold=0.75):
    for w in word_list:
        if similar(word, w) >= threshold:
            return True
    return False

def tokenize(text):
    return str(text).lower().split()


# ---------- Streamlit UI ----------
st.set_page_config(
    page_title="Domain ASR Error Detection",
    layout="wide"
)

st.title("🧠 Domain-Specific ASR Error Detection")
st.write(
    "Compare ASR transcript with corrected transcript and detect "
    "missing or mis-recognized **domain-specific words**."
)

# ---------- File Upload ----------
asr_file = st.file_uploader(
    "Upload ASR Transcript (Excel)", type=["xlsx"]
)
corrected_file = st.file_uploader(
    "Upload Corrected Transcript (Excel)", type=["xlsx"]
)
domain_file = st.file_uploader(
    "Upload Domain Dictionary (Excel)", type=["xlsx"]
)

# ---------- Processing ----------
if asr_file and corrected_file and domain_file:

    asr_df = pd.read_excel(asr_file)
    corr_df = pd.read_excel(corrected_file)
    domain_df = pd.read_excel(domain_file)

    # Take first column only
    domain_words = set(
        domain_df.iloc[:, 0].astype(str).str.lower().str.strip()
    )

    errors = []

    row_limit = min(len(asr_df), len(corr_df))

    for i in range(row_limit):

        asr_text = asr_df.iloc[i, 0]
        corr_text = corr_df.iloc[i, 0]

        asr_tokens = tokenize(asr_text)
        corr_tokens = tokenize(corr_text)

        missing_domain_words = []

        for dword in domain_words:
            # Present in corrected but NOT in ASR (even fuzzy)
            if dword in corr_tokens and not exists_similar(dword, asr_tokens):
                missing_domain_words.append(dword)

        if missing_domain_words:
            errors.append({
                "Row": i + 1,
                "Corrected_Text": corr_text,
                "ASR_Text": asr_text,
                "Missing_Domain_Words": ", ".join(missing_domain_words)
            })

    # ---------- Output ----------
    st.subheader("📌 Detected Domain Errors")

    if errors:
        error_df = pd.DataFrame(errors)
        st.dataframe(error_df, use_container_width=True)
        st.success(f"{len(error_df)} rows with domain-specific ASR errors detected")
    else:
        st.info("No domain-specific ASR errors found")

else:
    st.warning("⚠️ Please upload **all three files** to continue")
