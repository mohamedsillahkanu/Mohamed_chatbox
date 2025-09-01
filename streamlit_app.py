import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def apply_blue_theme():
    """Apply custom blue theme styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(90deg, #1e40af, #3b82f6, #60a5fa);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Custom container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Image container */
    .image-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(5px);
    }
    
    /* Chat messages styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        margin: 0.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
    }
    
    /* User message */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0) !important;
        border-left: 4px solid #3b82f6 !important;
    }
    
    /* Input box styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 25px !important;
        border: 2px solid #3b82f6 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stChatInput {
        background: transparent !important;
        border: none !important;
        color: #1f2937 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6) !important;
    }
    
    /* Error and success messages */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    /* Welcome message */
    .welcome-message {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(59, 130, 246, 0.3);
        border-radius: 50%;
        border-top-color: #3b82f6;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def load_image():
    """Load and display the ICF SL image with enhanced styling"""
    try:
        image_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/726bcf69bf5539b005011a0bfd7ebc91a4b29a06/icf_sl%20(1).jpg"
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            
            # Create image container with custom styling
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(image, caption="🏢 ICF Sierra Leone", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Failed to load image")
    except Exception as e:
        st.error(f"❌ Error loading image: {e}")

def show_welcome_message():
    """Display a welcome message with features"""
    st.markdown("""
    <div class="welcome-message">
        <h3>🤖 Welcome to ICF-SL AI Assistant!</h3>
        <p>I'm here to help you with information about ICF Sierra Leone. Feel free to ask me anything!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>💼 Services</h4>
            <p>Learn about our consulting services and expertise</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🌍 Projects</h4>
            <p>Discover our projects and impact in Sierra Leone</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📞 Contact</h4>
            <p>Get in touch with our team for inquiries</p>
        </div>
        """, unsafe_allow_html=True)

def initialize_chat():
    """Initialize the chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display existing chat messages with enhanced styling"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(client):
    """Process user input and generate response"""
    prompt = st.chat_input("💬 Ask me anything about ICF Sierra Leone...")
    
    if prompt:
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # Show loading indicator
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Generate AI response
                    stream = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful AI assistant for ICF Sierra Leone, a consulting company. Provide informative and professional responses about the company, its services, projects, and general inquiries. Be friendly and helpful."},
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                        temperature=0.7,
                    )
                    
                    response = st.write_stream(stream)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")
            st.info("💡 Please check your OpenAI API key and try again.")

def main():
    # Configure page
    st.set_page_config(
        page_title="ICF-SL AI Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply blue theme
    apply_blue_theme()
    
    # Main title with custom styling
    st.markdown('<h1 class="main-title">🤖 ICF-SL AI Assistant</h1>', unsafe_allow_html=True)
    
    # Create main container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Load image
    load_image()
    
    try:
        # Get API key from secrets
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        
        # Initialize OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Initialize chat session
        initialize_chat()
        
        # Show welcome message if no chat history
        if not st.session_state.messages:
            show_welcome_message()
        
        # Display chat history
        display_chat_history()
        
        # Handle user input
        handle_user_input(client)
        
    except KeyError:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef2f2, #fee2e2); 
                    padding: 1.5rem; border-radius: 10px; border-left: 5px solid #ef4444;">
            <h4>🔑 API Key Required</h4>
            <p>OpenAI API key not found. Please add it to your Streamlit secrets.</p>
            <p><strong>Instructions:</strong></p>
            <ol>
                <li>Go to your Streamlit app settings</li>
                <li>Add your OpenAI API key in secrets.toml</li>
                <li>Format: <code>OPENAI_API_KEY = "your-api-key-here"</code></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; 
                background: rgba(255,255,255,0.1); border-radius: 10px;">
        <p style="color: #ffffff; font-size: 0.9rem;">
            💼 Powered by ICF Sierra Leone | Built with ❤️ using Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
