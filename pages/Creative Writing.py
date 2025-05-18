import requests
import streamlit as st

st.title("Check your grammar!")

tab1,tab2, = st.tabs(["Get a random word","Grammar Check"])  # Comma is important for tuple unpacking

with tab1:
    sentence = st.text_area("Enter the sentence that you've written to check for any mistakes:", height=150)

import streamlit as st
import pandas as pd
import random

# Replace this with your actual raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/username/repo/main/words.csv"

@st.cache_data
def load_words(url):
    df = pd.read_csv(url)
    return df

st.title("Random Word Suggester")

try:
    df = load_words(CSV_URL)
    if "word" not in df.columns:
        st.error("CSV must have a 'word' column.")
    else:
        if st.button("Suggest a Random Word"):
            word = random.choice(df["word"].dropna().tolist())
            st.success(f"Your random word is: **{word}**")
except Exception as e:
    st.error(f"Failed to load CSV: {e}")



with tab2:
    sentence = st.text_area("Enter the sentence that you've written to check for any mistakes:", height=150)

    if st.button("Check Grammar"):
        if sentence.strip():
            url = "https://api.languagetool.org/v2/check"
            data = {
                'text': sentence,
                'language': 'en-US'
            }
            response = requests.post(url, data=data)
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
                    
                    # Safely get replacements
                    replacements = match.get('replacements', [])
                    suggestion = ', '.join([r['value'] for r in replacements]) if replacements else 'No suggestion'
                    
                    st.markdown(
                        f"**Issue {i}:** {match.get('message', 'Unknown error')}\n\n"
                        f"- **Error:** `{error_part}`\n"
                        f"- **Suggestion:** `{suggestion}`\n"
                        f"- **Rule:** {match.get('rule', {}).get('description', 'Unknown rule')}\n"
                    )
        else:
            st.warning("Please enter some text.")
