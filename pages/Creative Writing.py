import openai
import streamlit as st

openai.api_key = "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"

st.title("GPT Grammar Checker")

text = st.text_area("Enter text to check:")

if st.button("Check Grammar"):
    if text.strip():
        prompt = f"Correct any grammar, spelling, or style mistakes in the following text and explain your corrections:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0
        )
        st.write(response['choices'][0]['message']['content'])
    else:
        st.warning("Please enter some text.")
