import streamlit as st
import language_tool_python

def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    return matches

st.title("Grammar Checker App")
st.write("Enter a sentence to check its grammatical correctness:")

text_input = st.text_area("Input Text", height=150)

if st.button("Check Grammar"):
    if text_input.strip():
        with st.spinner("Analyzing..."):
            matches = check_grammar(text_input)
            
        if not matches:
            st.success("✅ The sentence is grammatically correct!")
        else:
            st.error(f"❌ Found {len(matches)} potential error(s)")
            
            for i, match in enumerate(matches, 1):
                st.markdown(f"""
                **Error {i}**  
                - **Message**: {match.message}  
                - **Suggested Correction**: {', '.join(match.replacements)}  
                - **Context**: `...{text_input[max(0, match.offset-10):match.offset]}**{text_input[match.offset:match.offset+match.errorLength]}**{text_input[match.offset+match.errorLength:match.offset+match.errorLength+10]}...`
                """)
    else:
        st.warning("Please enter some text to check")
