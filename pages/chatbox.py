import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def load_image():
    """Load and display the ICF SL image"""
    try:
        image_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/726bcf69bf5539b005011a0bfd7ebc91a4b29a06/icf_sl%20(1).jpg"
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="ICF SL Image", use_container_width=True)
        else:
            st.error("Failed to load image")
    except Exception as e:
        st.error(f"Error loading image: {e}")

def initialize_chat():
    """Initialize the chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display existing chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(client):
    """Process user input and generate response"""
    prompt = st.chat_input("🤖 ICF-SL AI Assistant. What would you like to know?")
    
    if prompt:
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display AI response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    # Set page title
    st.title("💬 Mohamed's Chatbot")
    
    # Load image
    load_image()
    
    
    
    if not openai_api_key:
        st.info("Please enter your OpenAI API key", icon="🗝️")
    else:
        # Initialize OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Initialize chat session
        initialize_chat()
        
        # Display chat history
        display_chat_history()
        
        # Handle user input
        handle_user_input(client)

if __name__ == "__main__":
    main()
