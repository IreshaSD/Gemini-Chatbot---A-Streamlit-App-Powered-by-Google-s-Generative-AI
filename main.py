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
if "chat_response_count" not in st.session_state:
    st.session_state.chat_response_count = 0

if "chat_responses" not in st.session_state:
    st.session_state.chat_responses = []

if "chat_initial_response_received" not in st.session_state:
    st.session_state.chat_initial_response_received = False

if "chat_user_prompt" not in st.session_state:
    st.session_state.chat_user_prompt = ""

# Function to reset the response count for ChatBot
def reset_chat_response_count():
    st.session_state.chat_response_count = 0
    st.session_state.chat_responses = []
    st.session_state.chat_initial_response_received = False
    st.session_state.chat_user_prompt = ""

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
        st.session_state.chat_user_prompt = user_prompt
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        st.session_state.chat_responses.append(gemini_response.text)
        st.session_state.chat_response_count = len(st.session_state.chat_responses) - 1
        st.session_state.chat_initial_response_received = True

    if st.session_state.chat_initial_response_received:
        st.markdown(st.session_state.chat_responses[st.session_state.chat_response_count])

        if st.session_state.chat_response_count == 0 and len(st.session_state.chat_responses) < 3:
            if st.button("Get Another Response"):
                gemini_response = st.session_state.chat_session.send_message(st.session_state.chat_user_prompt)
                st.session_state.chat_responses.append(gemini_response.text)
                st.session_state.chat_response_count = len(st.session_state.chat_responses) - 1

        if st.session_state.chat_response_count == 1 and len(st.session_state.chat_responses) < 3:
            if st.button("Get One More Response"):
                gemini_response = st.session_state.chat_session.send_message(st.session_state.chat_user_prompt)
                st.session_state.chat_responses.append(gemini_response.text)
                st.session_state.chat_response_count = len(st.session_state.chat_responses) - 1

        if st.session_state.chat_response_count > 0:
            if st.button("Previous Response"):
                if st.session_state.chat_response_count > 0:
                    st.session_state.chat_response_count -= 1
                    st.markdown(st.session_state.chat_responses[st.session_state.chat_response_count])

        if st.session_state.chat_response_count < len(st.session_state.chat_responses) - 1:
            if st.button("Next Response"):
                if st.session_state.chat_response_count < len(st.session_state.chat_responses) - 1:
                    st.session_state.chat_response_count += 1
                    st.markdown(st.session_state.chat_responses[st.session_state.chat_response_count])

# Image Captioning page
if selected == "Image Captioning":
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            col1, col2, col3 = st.columns(3)

            with col1:
                resized_image = image.resize((800, 500))
                st.image(resized_image)

            with col2:
                st.subheader("Short Description")
                short_prompt = "Write a short caption for this image"
                short_caption = gemini_pro_vision_response(short_prompt, image)
                st.info(short_caption)

            with col3:
                st.subheader("Detailed Description")
                long_prompt = "Write a detailed description for this image"
                long_caption = gemini_pro_vision_response(long_prompt, image)
                st.info(long_caption)
        else:
            st.error("No image detected. Please upload an image for captioning and try again.")

# Text embedding page
if selected == "Embed text":
    st.title("🔡 Embed Text")

    user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

    if st.button("Get Response"):
        if user_prompt.strip() == "":
            st.error("No text entered. Please input text to get embeddings.")
        else:
            response = embeddings_model_response(user_prompt)
            st.markdown(response)

# Question answering page
if selected == "Ask me anything":
    st.title("❓ Ask me a question")

    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        if user_prompt.strip() == "":
            st.error("No question entered. Please ask a question to get a response.")
        else:
            response = gemini_pro_response(user_prompt)
            st.markdown(response)




