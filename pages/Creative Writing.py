import streamlit as st
import language_tool_python

st.title("Simple Grammar Checker")

sentence = st.text_area("Enter a sentence to check:", height=100)

if st.button("Check Grammar"):
    if sentence.strip():
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(sentence)
        if len(matches) == 0:
            st.success("✅ The sentence is grammatically correct!")
        else:
            st.error(f"❌ Found {len(matches)} issue(s):")
            for match in matches:
                st.write(f"- {match.message}")
    else:
        st.warning("Please enter a sentence.")
