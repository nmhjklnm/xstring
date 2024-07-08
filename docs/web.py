import streamlit as st

st.set_page_config(page_title="Chat with the , powered by llm", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the LazyCat💬")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about Streamlit's open-source Python library!",
        }
    ]

# Fake data for testing purposes
fake_responses = [
    {
        "role": "assistant",
        "content": "Sure! Here's an example of how to create a simple Streamlit app:\n\n```python\nimport streamlit as st\n\nst.title('Hello, Streamlit!')\nst.write('This is a simple Streamlit app.')\n```",
    },
    {
        "role": "assistant",
        "content": "Streamlit allows you to create interactive web applications with Python. You can use widgets like sliders, buttons, and text inputs.",
    },
]

if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        # Generate a fake response
        fake_response = fake_responses[len(st.session_state.messages) % len(fake_responses)]
        st.write(fake_response["content"])
        # Add response to message history
        st.session_state.messages.append(fake_response)