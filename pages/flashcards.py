import streamlit as st

# Streamlit app code for interactive flashcards with flip-to-reveal functionality

def main():
    st.title('Interactive Flashcards')

    # Flashcards data
    cards = [
        {'word': 'Python', 'definition': 'A high-level programming language.'},
        {'word': 'JavaScript', 'definition': 'A scripting language for web development.'},
        {'word': 'HTML', 'definition': 'The standard markup language for creating web pages.'},
        {'word': 'CSS', 'definition': 'A style sheet language used for describing the presentation of a document.'},
        {'word': 'API', 'definition': 'Application Programming Interface.'}
    ]

    # State to track flipped cards
    if 'flipped' not in st.session_state:
        st.session_state.flipped = [False] * len(cards)

    # Display flashcards
    for i, card in enumerate(cards):
        if st.button(card['word'], key=f'card_{i}'):
            st.session_state.flipped[i] = not st.session_state.flipped[i]

        if st.session_state.flipped[i]:
            st.write(card['definition'])
        else:
            st.write('Click the word to see the definition')

if __name__ == '__main__':
    main()
