import streamlit as st
import requests

# Flask API endpoint (running locally in SageMaker)
API_URL = "http://127.0.0.1:5000/chat"

# --- Sidebar for user info ---
st.sidebar.title("👤 User Info")

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 0

st.session_state.user_name = st.sidebar.text_input("Enter your name", st.session_state.user_name)
st.session_state.user_age = st.sidebar.number_input("Enter your age", min_value=0, max_value=120, step=1)

# --- Show Chat UI only if name and age are given ---
if st.session_state.user_name and st.session_state.user_age > 0:
    st.title("💬 Health Assistant Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call Flask API
        payload = {
            "query": prompt,
            "name": st.session_state.user_name,
            "age": st.session_state.user_age
        }
        try:
            response = requests.post(API_URL, json=payload)
            data = response.json()
            bot_reply = data.get("response", "⚠️ No response")
            related_doctor = data.get("related_doctor", "")

            # Format assistant response
            final_reply = f"{bot_reply}\n\n👨‍⚕️ *Suggested Doctor:* {related_doctor}"

        except Exception as e:
            final_reply = f"⚠️ Error: {str(e)}"

        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": final_reply})
        with st.chat_message("assistant"):
            st.markdown(final_reply)

else:
    st.title("🩺 Health Assistant Chatbot")
    st.info("👉 Please enter your **name** and **age** in the sidebar to start chatting.")
