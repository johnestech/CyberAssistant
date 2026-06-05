import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title='CyberSecurity Assistant',page_icon='🛡️')

# Read api from local file or cloud
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are a cyber security assistant. You have decades of experience in cyber security, ethical hacking
and penetration testing. You have expertise in exploiting systems for the grater good to find dooeways,
find errors, and ways that the bad guys can exploit a system.
With your level of expertise, your task is to help users understand the vulnerabilites and exploits
that can be used on a system. You teach them about prompt injection, sql injections and every other
cyber security questions they have to ask. If they attach an image, you should analyse the image and
provide help on ways to fix their system, learn about something, or understand a problem better.

Be very helpful, professional, calm and respond politely
If you're asked any questions that is not related to your field of expertise, politely decline it.
Make sure you verify and information before responding to the user. Do not hallucinate and answer what
you dont know. If a question is asked that you have no idea what it is, politely say you don't know.
"""

st.title("Cyber Security Assistant🛡️")

if not api_key:
    st.error("GEMINI_API_KEY not found. Add it to your .env file or Streamlit secrets.")
    st.stop()

if "chat" not in st.session_state:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
    st.session_state.chat = model.start_chat()

for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        for part in msg.parts:
            if hasattr(part, "text") and part.text:
                st.markdown(part.text)

image_file = st.file_uploader("📷 Upload an image(optional)", type=["jpg", "jpeg", "png"])
user_input = st.chat_input("Ask anything about hacking or cyber security...")

if user_input:
    message = [user_input]
    if image_file:
        message.append(Image.open(image_file))

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(message, stream=True)
        st.write_stream(chunk.text for chunk in response if chunk.text)

    st.rerun()
