import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Custom CSS for black and blue theme with colorful responses
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f3a 50%, #0d1421 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1f3a;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        background-color: #1e293b !important;
        border: 2px solid #3b82f6 !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    
    /* User messages */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
        border-radius: 15px !important;
        border: 1px solid #60a5fa !important;
    }
    
    /* Assistant messages */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        border-radius: 15px !important;
        border: 1px solid #334155 !important;
    }
    
    /* Message text styling */
    .stChatMessage p {
        color: #e2e8f0 !important;
        font-size: 16px !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: linear-gradient(135deg, #1a1f3a, #0f1419) !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 10px !important;
        position: relative !important;
    }
    
    /* Copy button styling */
    .stCodeBlock button {
        background-color: red !important;
        color: red !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        opacity: 0.9 !important;
        transition: all 0.2s ease !important;
    }
    
    .stCodeBlock button:hover {
        background-color: #f3f4f6 !important;
        opacity: 1 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stCodeBlock button:active {
        background-color: #e5e7eb !important;
        transform: translateY(1px) !important;
    }
    
    /* Code syntax highlighting */
    .stCodeBlock code {
        background-color: transparent !important;
        font-family: 'Fira Code', 'Consolas', 'Monaco', monospace !important;
        line-height: 1.5 !important;
    }
    
    /* Python syntax highlighting */
    .stCodeBlock .hljs-keyword {
        color: #ff6b9d !important; /* Pink for keywords like def, if, for, import */
    }
    
    .stCodeBlock .hljs-string {
        color: #a8e6cf !important; /* Light green for strings */
    }
    
    .stCodeBlock .hljs-comment {
        color: #95a5a6 !important; /* Gray for comments */
        font-style: italic !important;
    }
    
    .stCodeBlock .hljs-function {
        color: #ffd93d !important; /* Yellow for function names */
    }
    
    .stCodeBlock .hljs-title {
        color: #ffd93d !important; /* Yellow for function/class names */
    }
    
    .stCodeBlock .hljs-built_in {
        color: #74b9ff !important; /* Light blue for built-ins like print, len */
    }
    
    .stCodeBlock .hljs-number {
        color: #fd79a8 !important; /* Pink for numbers */
    }
    
    .stCodeBlock .hljs-variable {
        color: #81ecec !important; /* Cyan for variables */
    }
    
    .stCodeBlock .hljs-params {
        color: #fab1a0 !important; /* Peach for parameters */
    }
    
    .stCodeBlock .hljs-attr {
        color: #e17055 !important; /* Orange for attributes */
    }
    
    .stCodeBlock .hljs-class {
        color: #a29bfe !important; /* Purple for classes */
    }
    
    .stCodeBlock .hljs-operator {
        color: #ff7675 !important; /* Red for operators */
    }
    
    .stCodeBlock .hljs-punctuation {
        color: #ddd6fe !important; /* Light purple for punctuation */
    }
    
    .stCodeBlock .hljs-literal {
        color: #fd79a8 !important; /* Pink for literals like True, False, None */
    }
    
    .stCodeBlock .hljs-type {
        color: #6c5ce7 !important; /* Purple for types */
    }
    
    .stCodeBlock .hljs-name {
        color: #00cec9 !important; /* Teal for names */
    }
    
    /* Default code text color */
    .stCodeBlock code,
    .stCodeBlock .hljs {
        color: #e2e8f0 !important; /* Light gray for default text */
    }
    
    /* Inline code */
    code:not(.hljs) {
        background-color: #1e293b !important;
        color: #fbbf24 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #3b82f6 !important;
        font-family: 'Fira Code', 'Consolas', 'Monaco', monospace !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #60a5fa !important;
        text-shadow: 0 0 10px #3b82f6 !important;
    }
    
    /* Lists */
    ul, ol {
        color: #e2e8f0 !important;
    }
    
    li {
        color: #cbd5e1 !important;
        margin-bottom: 5px !important;
    }
    
    /* Strong/bold text */
    strong, b {
        color: #fbbf24 !important;
        font-weight: bold !important;
    }
    
    /* Emphasis/italic text */
    em, i {
        color: #a78bfa !important;
        font-style: italic !important;
    }
    
    /* Links */
    a {
        color: #60a5fa !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: #93c5fd !important;
        text-shadow: 0 0 5px #3b82f6 !important;
    }
    
    /* Blockquotes */
    blockquote {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border-left: 4px solid #3b82f6 !important;
        color: #cbd5e1 !important;
        padding: 10px 15px !important;
        border-radius: 5px !important;
    }
    
    /* Tables */
    .stTable {
        background-color: #1e293b !important;
        border-radius: 10px !important;
    }
    
    table {
        color: #e2e8f0 !important;
    }
    
    th {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* Error/warning messages */
    .stAlert {
        background-color: #1e293b !important;
        border: 1px solid #3b82f6 !important;
        color: #e2e8f0 !important;
    }
    
    /* Metrics */
    .metric-container {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Pre-formatted text */
    pre {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        color: #60a5fa !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(45deg, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: bold;
        text-shadow: 0 0 20px #3b82f6;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def load_image():
    """Load and display the ICF SL image with reduced size"""
    try:
        image_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/726bcf69bf5539b005011a0bfd7ebc91a4b29a06/icf_sl%20(1).jpg"
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # Create columns to center and resize the image
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="ICF SL", width=300)
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
        
        try:
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
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

def main():
    # Set page title with custom styling
    st.markdown('<h1 class="main-title">Data Analytics Training Chatbot</h1>', unsafe_allow_html=True)
    
    # Load image
    load_image()
    
    try:
        # Get API key from secrets
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        
        # Initialize OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Initialize chat session
        initialize_chat()
        
        # Display chat history
        display_chat_history()
        
        # Handle user input
        handle_user_input(client)
        
    except KeyError:
        st.error("OpenAI API key not found. Please add it to your Streamlit secrets.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
