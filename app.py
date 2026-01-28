import streamlit as st
import pandas as pd
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def exists_similar(word, word_list, threshold=0.75):
    for w in word_list:
        if similar(word, w) >= threshold:
            return True
    return False


st.set_page_config(page_title="Domain ASR Error Detection", layout="wide")

st.title("📞 Domain-Specific ASR Error Detection")
st.write("Compare ASR transcript with corrected transcript and detect domain errors")

# Upload files
asr_file = st.file_uploader("Upload ASR Transcript (Excel)", type=["xlsx"])
corrected_file = st.file_uploader("Upload Corrected Transcript (Excel)", type=["xlsx"])
domain_file = st.file_uploader("Upload Domain Dictionary (Excel)", type=["xlsx"])

if asr_file and corrected_file and domain_file:
    asr_df = pd.read_excel(asr_file)
    corr_df = pd.read_excel(corrected_file)
    domain_df = pd.read_excel(domain_file)

    st.subheader("🔍 Detected Domain Errors")

    domain_words = set(domain_df.iloc[:, 0].astype(str).str.lower())

    errors = []

    for i in range(min(len(asr_df), len(corr_df))):
        asr_text = str(asr_df.iloc[i, 0]).lower()
        corr_text = str(corr_df.iloc[i, 0]).lower()

       missing_domain_words = []

for dword in domain_words:
    if dword in corr_words and not exists_similar(dword, asr_words):
        missing_domain_words.append(dword)

                })

    if errors:
        error_df = pd.DataFrame(errors)
        st.dataframe(error_df, use_container_width=True)
        st.success(f"✅ {len(error_df)} domain errors detected")
    else:
        st.info("🎉 No domain-specific errors found")
else:
    st.warning("⬆️ Please upload all three files")
