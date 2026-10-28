import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# If you get a "model not found" error, check AI Studio
# for a current Flash model name and paste it here
MODEL = "gemini-3-flash-preview"

st.set_page_config(
    page_title="SmartChat - Teaching Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("SmartChat")
st.caption("Your friendly assistant for maths and computing lessons.")

if not api_key:
    st.error("API key not found. Please add GEMINI_API_KEY to your .env file.")
    st.stop()

# We use the OpenAI library, but point it to Google's server
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are SmartChat, a helpful teaching assistant for a tutor
who teaches maths and computing to students in the UK.

Your role is to help the tutor prepare lessons and support students.

When answering:
- Explain ideas clearly, one step at a time.
- Use simple language and relatable examples.
- Adjust explanations to the student's age and level.
- Create practice questions and provide answers when requested.
- Be honest if you are unsure about something.
- Do not make up facts or information.
"""

# Keep the conversation available while the app is running
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Conversation")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display earlier messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Let the user ask a new question
prompt = st.chat_input("Ask a question about maths or computing...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ],
                stream=True
            )

            answer = st.write_stream(response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(
                "Sorry, I couldn't generate a response. "
                f"Details: {e}"
            )