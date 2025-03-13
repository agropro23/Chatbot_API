import streamlit as st
from groq import Groq

# Set up the page
st.set_page_config(page_title="Simple Groq Chatbot", layout="centered")
st.title("Simple Groq Chatbot")
st.write("Select a model and start chatting.")

# Let the user pick a Groq model
model = st.selectbox("Select model", ["llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama3-70b-8192"])

# Initialize the Groq client with the API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key="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")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user's message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Show a spinner while the assistant responds
    with st.spinner("Thinking..."):
        try:
            # Call the Groq API to get a response
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                stream=False
            )
            # Extract the assistant's reply
            msg = response.choices[0].message.content
            # Add it to the chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
        except Exception as e:
            st.error(f"Oops, something went wrong: {e}")