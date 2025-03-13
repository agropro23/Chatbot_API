import streamlit as st
from groq import Groq

# Sidebar for API key input
with st.sidebar:
    api_key_input = st.text_input("Enter your Groq API Key", type="password")
    if st.button("Set API Key"):
        if api_key_input:
            st.session_state["api_key"] = api_key_input
            st.success("API Key set successfully!")
        else:
            st.warning("Please enter a valid API key.")

# Main app logic
if "api_key" in st.session_state:
    try:
        # Initialize Groq client with the API key from session state
        client = Groq(api_key=st.session_state["api_key"])
        
        st.title("Simple Groq Chatbot")
        st.write("Select a model and start chatting.")
        
        # Model selection
        model = st.selectbox("Select model", ["llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama3-70b-8192"])
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]
        
        # Display chat history
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        # Handle user input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # Get response from Groq API
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=st.session_state.messages,
                        stream=False
                    )
                    msg = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    st.chat_message("assistant").write(msg)
                except Exception as e:
                    st.error(f"Oops, something went wrong: {e}")
    except Exception as e:
        st.error("Invalid API key or unable to initialize Groq client. Please check your API key.")
else:
    st.write("Please enter your Groq API Key in the sidebar to start chatting.")