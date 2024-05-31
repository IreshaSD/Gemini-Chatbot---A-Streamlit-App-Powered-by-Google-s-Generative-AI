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

# Chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  # Renamed for clarity
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro...")  # Renamed for clarity
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)  # Renamed for clarity

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image Captioning page
if selected == "Image Captioning":
    # Streamlit page title
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            col1, col2, col3 = st.columns(3)

            with col1:
                resized_image = image.resize((800, 500))
                st.image(resized_image)

            # Short description
            short_prompt = "Write a short caption for this image"  # change this prompt as per your requirement
            short_caption = gemini_pro_vision_response(short_prompt, image)
            with col2:
                st.info(short_caption)

            # Longer description
            long_prompt = "Write a detailed description for this image"  # change this prompt as per your requirement
            long_caption = gemini_pro_vision_response(long_prompt, image)
            with col3:
                st.info(long_caption)
        else:
            st.error("No image detected. Please upload an image for captioning and try again.")

# Text embedding page
if selected == "Embed text":
    st.title("🔡 Embed Text")

    # Text box to enter prompt
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

    # Text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        if user_prompt.strip() == "":
            st.error("No question entered. Please ask a question to get a response.")
        else:
            response = gemini_pro_response(user_prompt)
            st.markdown(response)

