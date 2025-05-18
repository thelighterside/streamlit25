import requests
import streamlit as st

st.title("Simple Grammar Checker Using LanguageTool API")

sentence = st.text_area("Enter a sentence to check:", height=100)

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
        if len(matches) == 0:
            st.success("✅ The sentence is grammatically correct!")
        else:
            st.error(f"❌ Found {len(matches)} issue(s):")
            for match in matches:
                st.write(f"- {match['message']}")
    else:
        st.warning("Please enter a sentence.")
