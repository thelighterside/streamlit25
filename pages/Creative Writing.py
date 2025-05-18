import requests
import streamlit as st

st.title("Enhanced Grammar Checker Using LanguageTool API")

sentence = st.text_area("Enter your text to check:", height=150)

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
                context = match['context']
                offset = context['offset']
                length = context['length']
                context_text = context['text']
                error_part = context_text[offset:offset+length]
                st.markdown(
                    f"**Issue {i}:** {match['message']}\n\n"
                    f"- **Error:** `{error_part}`\n"
                    f"- **Suggestion:** `{', '.join(match['replacements']) if match['replacements'] else 'No suggestion'}`\n"
                    f"- **Rule:** {match['rule']['description']}\n"
                )
    else:
        st.warning("Please enter some text.")
