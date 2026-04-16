import os
import sys
from dataclasses import dataclass
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv


@dataclass
class ChatMessage:
    role: str
    text: str


def detect_language(text: str) -> str:
    lowered = text.lower()
    tr_markers = ["ğ", "ş", "ı", "ç", "ö", "ü", "mi ", "mı ", "mu ", "mü "]
    if any(marker in lowered for marker in tr_markers):
        return "tr"
    return "en"


def parse_language_command(command: str, current_language: str) -> str:
    parts = command.split()
    if len(parts) == 1:
        return current_language
    choice = parts[1].lower()
    if choice in {"tr", "turkish"}:
        return "tr"
    if choice in {"en", "english"}:
        return "en"
    if choice == "auto":
        return "auto"
    return current_language


def print_help() -> None:
    print("\nCommands:")
    print("- help                : Show this help menu.")
    print("- clear               : Clear chat history.")
    print("- history             : List chat history.")
    print("- language            : Show current language mode (tr/en/auto).")
    print("- language tr|en|auto : Change language mode.")
    print("- exit                : Exit the program.\n")


def build_prompt(user_text: str, selected_language: str) -> str:
    if selected_language == "tr":
        return f"Please respond only in Turkish:\n{user_text}"
    if selected_language == "en":
        return f"Please respond only in English:\n{user_text}"
    detected = detect_language(user_text)
    if detected == "tr":
        return f"Please respond only in Turkish:\n{user_text}"
    return f"Please respond only in English:\n{user_text}"


def print_history(chat_history: List[ChatMessage]) -> None:
    if not chat_history:
        print("Chat history is empty.")
        return
    print("\nChat History:")
    for idx, message in enumerate(chat_history, start=1):
        speaker = "User" if message.role == "user" else "Bot"
        print(f"{idx}. {speaker}: {message.text}")
    print("")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please add it to your .env file.")
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception as exc:
        print(f"Error: Failed to initialize Gemini client ({exc})")
        sys.exit(1)

    print("Welcome to Suna's Chatbot! (type 'help' for commands)\n")
    language_mode = "auto"
    chat_history: List[ChatMessage] = []

    while True:
        prompt = input("User: ").strip()
        command = prompt.lower()

        if command == "exit":
            print("See you later :)")
            break
        if not prompt:
            continue
        if command == "help":
            print_help()
            continue
        if command == "clear":
            chat_history.clear()
            print("Chat history cleared.")
            continue
        if command == "history":
            print_history(chat_history)
            continue
        if command.startswith("language"):
            previous_language = language_mode
            language_mode = parse_language_command(command, language_mode)
            if language_mode == previous_language and command != "language":
                print("Invalid language choice. Use: language tr|en|auto")
            else:
                print(f"Active language mode: {language_mode}")
            continue

        final_prompt = build_prompt(prompt, language_mode)
        chat_history.append(ChatMessage(role="user", text=prompt))

        try:
            response = model.generate_content(final_prompt)
            response_text = (response.text or "").strip()
            if not response_text:
                response_text = "Received an empty response. Please try again."
            chat_history.append(ChatMessage(role="bot", text=response_text))
            print("Bot:", response_text)
        except Exception as exc:
            print(f"Error: API did not respond or the key may be invalid ({exc})")


if __name__ == "__main__":
    main()
