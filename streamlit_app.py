# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st

openai.api_type = "azure"
openai.api_version = "2023-05-15" 
COMPLETION_MODEL = "basicGPT35"

with st.sidebar:
    st.title('🤖💬 Hello, This is Tina Chatbot')

    if 'OPENAI_API_BASE' in st.secrets:
        st.success('API base URL already provided!', icon='✅')
        openai.api_base = st.secrets['OPENAI_API_BASE']
    else:
        openai.api_base = st.text_input('Enter API base URL:', type='default')
        if not (openai.api_base.startswith('https://tina')):
            st.warning('Please enter your base URL!', icon='⚠️')
        else:
            st.success('Proceed to entering your credentials!', icon='👇')

    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (len(openai.api_key)==33):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            engine=COMPLETION_MODEL,
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
