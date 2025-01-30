import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Show title and description.
st.title("💬 ICF-SL Chatbot")

# Add the image with enhanced styling
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


openai_api_key = "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"

if not openai_api_key:
    st.info("", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("🤖 ICF-SL AI Assistant. What would you like to know?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
