from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="Custom Gemini Q&A", page_icon="🌟", layout="wide")

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Custom theme styling
custom_theme = {
    "primaryColor": "#3498db",
    "backgroundColor": "#ecf0f1",
    "secondaryBackgroundColor": "#bdc3c7",
    "textColor": "#2c3e50",
    "font": "sans-serif",
}

# Set custom CSS styles
st.markdown(
    """
    <style>
        body {
            color: """ + custom_theme["textColor"] + """;
            background-color: """ + custom_theme["backgroundColor"] + """;
            font-family: """ + custom_theme["font"] + """;
        }
        .css-1l02zca {
            font-size: 24px !important;
            color: #e74c3c !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for chat history
st.sidebar.title("Chat History")

# Continue with the rest of your Streamlit app...

st.header("Welcome to the Custom Gemini Chat")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Ask me anything: ", key="input")
submit = st.button("Get Answer")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("User", input))
    st.sidebar.subheader("Bot's Response")
    for chunk in response:
        st.sidebar.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the main chat content
st.subheader("Chat History")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
