import os
from typing import List, Dict

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv


def detect_language(text: str) -> str:
    lowered = text.lower()
    tr_markers = ["ğ", "ş", "ı", "ç", "ö", "ü", "mi ", "mı ", "mu ", "mü "]
    if any(marker in lowered for marker in tr_markers):
        return "tr"
    return "en"


def build_prompt(user_text: str, selected_language: str) -> str:
    if selected_language == "tr":
        return f"Please respond only in Turkish:\n{user_text}"
    if selected_language == "en":
        return f"Please respond only in English:\n{user_text}"
    detected = detect_language(user_text)
    if detected == "tr":
        return f"Please respond only in Turkish:\n{user_text}"
    return f"Please respond only in English:\n{user_text}"


def get_model() -> genai.GenerativeModel:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def main() -> None:
    st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
    st.title("Gemini Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages: List[Dict[str, str]] = []
    if "language_mode" not in st.session_state:
        st.session_state.language_mode = "auto"

    st.session_state.language_mode = st.selectbox(
        "Language Mode",
        options=["auto", "tr", "en"],
        index=["auto", "tr", "en"].index(st.session_state.language_mode),
        help="When auto is selected, language is detected from user input.",
    )

    if st.button("Clear History"):
        st.session_state.messages = []
        st.success("Chat history cleared.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        model = get_model()
        final_prompt = build_prompt(user_input, st.session_state.language_mode)
        response = model.generate_content(final_prompt)
        response_text = (response.text or "").strip() or "Received an empty response."
    except Exception as exc:
        response_text = f"Error: API did not respond or the key may be invalid ({exc})"

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)


if __name__ == "__main__":
    main()
