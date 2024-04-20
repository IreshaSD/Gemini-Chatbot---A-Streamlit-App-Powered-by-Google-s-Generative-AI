import streamlit
import os
import json

import google.generativeai as genai

# Working directory path
working_directory = os.path.dirname(os.path.abspath(__file__))  # os.path.abspath(__file__): This function returns the absolute path of the current Python script file without resolving symbolic links. It simply resolves any relative paths and returns the absolute path as it appears in the filesystem.

# path of config_data file 
config_file_path = f"{working_directory}/config.json"
config_data = json.load(open("config.json"))


# Loading the API key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]


# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)


# function to load gemini-pro-model for chatbot
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")  # gemini pro takes input as text and it will give output as text also
    return gemini_pro_model


# Function for image captioning
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_modl = genai.GenerativeModel("gemini-pro-vision")  # gemini pro vision is a multimodel. It takes  text and as well as images as inputs but it gives the  output as text.
    response = gemini_pro_vision_modl.generate_content([prompt, image])
    result = response.text
    return result


# Image loading part for testing
# from PIL import Image
# image = Image.open("nature.jpg")
# prompt = "Write a BRIEF caption for this image"
# output = gemini_pro_vision_response(prompt,image)
# print(output)

# Similarly Embeding will take the input as text and returns embedding
# Funnction to get embedings for text
def embedding_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list





# Function to get a response from gemini-pro LLM
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result

