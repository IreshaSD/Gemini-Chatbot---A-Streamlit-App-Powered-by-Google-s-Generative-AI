import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response,
                            embeddings_model_response)

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Setting up the page configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Gemini AI',
                           ['ChatBot',
                            'Image Captioning',
                            'Embed text',
                            'Ask me anything'],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0
                           )

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Initialize response tracker for "ChatBot" if not already present
if "chat_questions" not in st.session_state:
    st.session_state.chat_questions = []

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = -1

if "current_response_index" not in st.session_state:
    st.session_state.current_response_index = 0

# Function to reset the response count for ChatBot
def reset_chat_state():
    st.session_state.chat_questions = []
    st.session_state.current_question_index = -1
    st.session_state.current_response_index = 0

# Chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    if st.session_state.chat_session is None:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 ChatBot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask Gemini-Pro...")
    if user_prompt:
        # Start a new question
        st.session_state.current_question_index += 1
        st.session_state.current_response_index = 0
        st.chat_message("user").markdown(user_prompt)
        
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        
        # Append the new question and its first response
        st.session_state.chat_questions.append({
            "prompt": user_prompt,
            "responses": [gemini_response.text]
        })

    if st.session_state.current_question_index >= 0:
        current_question = st.session_state.chat_questions[st.session_state.current_question_index]
        st.markdown(current_question["responses"][st.session_state.current_response_index])

        if st.session_state.current_response_index == 0 and len(current_question["responses"]) < 3:
            if st.button("Get Another Response"):
                gemini_response = st.session_state.chat_session.send_message(current_question["prompt"])
                current_question["responses"].append(gemini_response.text)
                st.session_state.current_response_index = len(current_question["responses"]) - 1

        if st.session_state.current_response_index == 1 and len(current_question["responses"]) < 3:
            if st.button("Get One More Response"):
                gemini_response = st.session_state.chat_session.send_message(current_question["prompt"])
                current_question["responses"].append(gemini_response.text)
                st.session_state.current_response_index = len(current_question["responses"]) - 1

        if st.session_state.current_response_index > 0:
            if st.button("Previous Response"):
                if st.session_state.current_response_index > 0:
                    st.session_state.current_response_index -= 1
                    st.markdown(current_question["responses"][st.session_state.current_response_index])

        if st.session_state.current_response_index < len(current_question["responses"]) - 1:
            if st.button("Next Response"):
                if st.sess




