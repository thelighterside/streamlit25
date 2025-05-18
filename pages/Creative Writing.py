import requests
import streamlit as st
import pandas as pd
import random

st.title("Check your grammar!")

tab1, tab2 = st.tabs(["Get a random word", "Grammar Check"])

# Corrected raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/thelighterside/streamlit25/main/data/group3_word_frequency.csv"

@st.cache_data
def load_words(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return None

with tab1:
    df = load_words(CSV_URL)
    if df is None:
        st.error("Failed to load CSV. Please check the file URL and make sure the file is public.")
    elif "word" not in df.columns:
        st.error("CSV must have a 'word' column.")
    else:
        if st.button("Suggest a Random Word"):
            word = random.choice(df["word"].dropna().tolist())
            st.success(f"Your random word is: **{word}**")

with tab2:
    sentence = st.text_area("Enter the sentence that you've written to check for any mistakes:", height=150)
    if st.button("Check Grammar"):
        if sentence.strip():
            url = "https://api.languagetool.org/v2/check"
            data = {
                'text': sentence,
                'language': 'en-US'
            }
            try:
                response = requests.post(url, data=data)
                response.raise_for_status()
                result = response.json()
                matches = result.get('matches', [])
                if not matches:
                    st.success("✅ No issues found! Your text looks good.")
                else:
                    st.error(f"❌ Found {len(matches)} issue(s):")
                    for i, match in enumerate(matches, 1):
                        context = match.get('context', {})
                        offset = context.get('offset', 0)
                        length = context.get('length', 0)
                        context_text = context.get('text', '')
                        error_part = context_text[offset:offset+length] if context_text else ''
                        replacements = match.get('replacements', [])
                        suggestion = ', '.join([r['value'] for r in replacements]) if replacements else 'No suggestion'
                        st.markdown(
                            f"**Issue {i}:** {match.get('message', 'Unknown error')}\n\n"
                            f"- **Error:** `{error_part}`\n"
                            f"- **Suggestion:** `{suggestion}`\n"
                            f"- **Rule:** {match.get('rule', {}).get('description', 'Unknown rule')}\n"
                        )
            except Exception as e:
                st.error(f"Grammar API error: {e}")
        else:
            st.warning("Please enter some text.")
