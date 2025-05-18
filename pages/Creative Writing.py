import requests
import streamlit as st
import pandas as pd
import random

st.title("Grammar & Vocabulary Helper")  # Single title at the top

tab1, tab2 = st.tabs(["Get a Random Word", "Grammar Check"])

# ===== TAB 1: Random Word =====
with tab1:
    CSV_URL = "https://raw.githubusercontent.com/thelighterside/streamlit25/refs/heads/main/data/group3_word_frequency.csv"
    
    @st.cache_data
    def load_words(url):
        return pd.read_csv(url)
    
    try:
        df = load_words(CSV_URL)
        if "word" not in df.columns:
            st.error("Error: CSV file must contain a 'word' column.")
        else:
            if st.button("Suggest a Random Word"):
                word = random.choice(df["word"].dropna().tolist())
                st.success(f"Your random word is: **{word}**")
    except Exception as e:
        st.error(f"Failed to load CSV: {str(e)}")

# ===== TAB 2: Grammar Check =====
with tab2:
    sentence = st.text_area("Enter your text to check for mistakes:", height=150)
    
    if st.button("Check Grammar"):
        if sentence.strip():
            url = "https://api.languagetool.org/v2/check"
            data = {'text': sentence, 'language': 'en-US'}
            
            try:
                response = requests.post(url, data=data)
                response.raise_for_status()  # Check for HTTP errors
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
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {str(e)}")
        else:
            st.warning("Please enter some text to check.")
