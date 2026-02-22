import streamlit as st
import requests
from langchain_core.messages import HumanMessage

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

user_input = st.chat_input("Type here")

for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

if user_input:
    st.session_state['message_history'].append({'role': "user", 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)

    response = requests.post(
        "http://localhost:8000/run",
        json={
            "messages": [{"type": "human", "content": user_input}],
            "config": {"configurable": {"thread_id": "1"}}
        }
    )

    reply = response.json()["output"]

    with st.chat_message("assistant"):
        st.text(reply)

    st.session_state['message_history'].append({'role': "assistant", 'content': reply})
