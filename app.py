import streamlit as st
import requests

# 🔑 Set your Gemini API Key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

def call_gemini_api(question):
    """
    Function to call Gemini API safely using requests
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": question}]}]}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

# 🎨 Streamlit UI
def run_chatbot():
    st.set_page_config(page_title="Material Selection Chatbot", layout="wide")
    st.title("🔧 AI Chatbot for Material Selection")
    st.write("Ask me anything about materials!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_query = st.chat_input("Enter your question here...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.chat_message("user"):
            st.write(user_query)

        with st.spinner("Thinking..."):
            answer = call_gemini_api(user_query)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.write(answer)

# Run the chatbot
if __name__ == "__main__":
    run_chatbot()
