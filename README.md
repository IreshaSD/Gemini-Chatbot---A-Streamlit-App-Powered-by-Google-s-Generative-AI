### Key Features:

1. Chat Interface: Engage in interactive conversations with the gemini-pro model through Streamlit's intuitive chat interface.
2. Image Captioning: Generate captions for uploaded images using the gemini-pro-vision model, extracting visual insights.
3. Text Embedding: Obtain numerical representations (embeddings) for input text, aiding in tasks like document similarity search.
4. Open-Ended Question Answering: Pose questions to the gemini-pro model and receive comprehensive responses, fostering knowledge exploration.

### Requirements:

1. Python 3.x (https://www.python.org/downloads/)
2. Streamlit (https://streamlit.io/)
3. Google Generative AI API Key ([invalid URL removed])

### Installation:

1. Clone this repository: git clone https://github.com/your-username/gemini-chatbot.git
2. Install dependencies: pip install streamlit google-generativeai
3. Obtain a Google Generative AI API key and store it securely.

### Explanation:

The main.py script is the core of the application. It handles:

  * API Key Loading: Reads the API key from the config.json file and configures the GenAI library.
  * Model Loading: Loads the gemini-pro and gemini-pro-vision models for chat and image captioning functionality.
  * Embedding Model: Defines a function to retrieve text embeddings using a pre-trained embedding model (replace with your preferred model name).
  * Chat Functionality: Implements the chat logic, managing chat history and interactions with the gemini-pro model using Streamlit's chat components.
  * Image Captioning: Uploads, resizes, and uses the gemini-pro-vision model to generate captions for images.
  * Text Embedding: Obtains embeddings for input text using the embedding_model_response function.
  * Question Answering: Processes user prompts and retrieves responses from the gemini-pro model.
  * Streamlit Integration: Creates a user-friendly interface using Streamlit's components like st.title, st.chat_message, st.button, text input areas, and image uploaders.
    
### Customization:

  * You can personalize the chatbot's responses by modifying the prompts used with the gemini-pro model.
  * Consider integrating additional GenAI models for specific tasks or explore custom embedding models for text.
