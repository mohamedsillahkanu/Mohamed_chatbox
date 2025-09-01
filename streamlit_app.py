import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def apply_blue_theme():
    """Apply custom dark blue and black theme styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #1a1a2e 100%);
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app styling */
    .main {
        background: transparent;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(90deg, #60a5fa, #3b82f6, #1d4ed8, #1e40af);
        background-size: 300% 300%;
        animation: gradient 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Custom container */
    .chat-container {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 0 0 1px rgba(59, 130, 246, 0.1),
            0 20px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* Image container */
    .image-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgba(30, 41, 59, 0.6);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat messages styling */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.7) !important;
        border-radius: 16px !important;
        margin: 0.8rem 0 !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        color: #e2e8f0 !important;
    }
    
    /* User message */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #1e40af, #1d4ed8, #2563eb) !important;
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 4px 20px rgba(29, 78, 216, 0.4) !important;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border-left: 4px solid #3b82f6 !important;
        color: #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Input box styling */
    .stChatInputContainer {
        background: rgba(15, 23, 42, 0.9) !important;
        border-radius: 25px !important;
        border: 2px solid #3b82f6 !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 
            0 0 0 1px rgba(59, 130, 246, 0.3),
            0 8px 32px rgba(0, 0, 0, 0.4) !important;
    }
    
    .stChatInput {
        background: transparent !important;
        border: none !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    .stChatInput::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af, #2563eb, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 0 0 1px rgba(59, 130, 246, 0.3),
            0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 0 0 1px rgba(59, 130, 246, 0.5),
            0 8px 25px rgba(59, 130, 246, 0.6) !important;
        background: linear-gradient(135deg, #2563eb, #3b82f6, #60a5fa) !important;
    }
    
    /* Error and success messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border-left: 4px solid #ef4444 !important;
        color: #fecaca !important;
    }
    
    /* Welcome message */
    .welcome-message {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.6));
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border-left: 5px solid #3b82f6;
        box-shadow: 
            0 0 0 1px rgba(59, 130, 246, 0.2),
            0 8px 32px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(15px);
        color: #e2e8f0;
    }
    
    .welcome-message h3 {
        color: #60a5fa;
        margin-bottom: 1rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(51, 65, 85, 0.4));
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        color: #e2e8f0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 0 0 1px rgba(59, 130, 246, 0.4),
            0 12px 40px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .feature-card h4 {
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    /* Text styling */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        border-radius: 10px;
        border: 2px solid rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb, #60a5fa);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 24px;
        height: 24px;
        border: 3px solid rgba(59, 130, 246, 0.3);
        border-radius: 50%;
        border-top-color: #3b82f6;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Spinner styling */
    .stSpinner {
        color: #3b82f6 !important;
    }
    
    /* Footer styling */
    .footer {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
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
                            {"role": "system", "content": "You are a helpful AI assistant for ICF Sierra Leone, a consulting company. Provide informative and professional responses about the company, its services, projects, and general inquiries. Be friendly and helpful."}
                        ] + [
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
    <div class="footer" style="text-align: center; margin-top: 2rem; padding: 1.5rem;">
        <p style="color: #60a5fa; font-size: 0.95rem; font-weight: 500;">
            💼 Powered by ICF Sierra Leone | Built with ❤️ using Streamlit & OpenAI
        </p>
        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem;">
            🌟 Advanced AI Assistant for Professional Consulting Services
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
