import streamlit as st
import language_tool_python

st.title("Grammar Checker (language_tool_python)")

sentence = st.text_area("Enter a sentence to check:", height=100)

if st.button("Check Grammar"):
    if sentence.strip():
        try:
            tool = language_tool_python.LanguageTool('en-US')
            matches = tool.check(sentence)
            if not matches:
                st.success("✅ The sentence is grammatically correct!")
            else:
                st.error(f"❌ Found {len(matches)} issue(s):")
                for match in matches:
                    st.write(f"- {match.message}")
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure Java 17 or higher is installed and available in your PATH.")
    else:
        st.warning("Please enter a sentence.")
