import streamlit as st
from core.config import config
import requests
#--------------------------------------------------------------
def api_call(method, url, **kwargs):

    def _show_error_popup(message):
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message
        }

    try:
        response = getattr(requests, method)(url, **kwargs)
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid response format from server"}

        if response.ok:
            return True, response_data
        return False, response_data
    except requests.exceptions.ConnectionError:
        _show_error_popup("Connection error. Check your network connection.")
        return False,  {"message": "Connection error"}
    except requests.exceptions.Timeout:
        _show_error_popup("Request Timeout")
        return False,  {"message": "Request Timeout"}
    except Exception as e:
        _show_error_popup(f"Unexpected error occured: {str(e)}")
        return False,  {"message": str(e)}
#--------------------------------------------------------------
with st.sidebar:
    st.title("Settings")
    st.session_state.provider = st.selectbox("Select LLM Provider", ["openai"])
    st.session_state.model_name = st.selectbox("Model Name", ["gpt-5-nano", "gpt-5-mini"])
#--------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{ "role": "assistant", "content": "Hello! How can I assist you today?" }]
#--------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
#--------------------------------------------------------------
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({ "role": "user", "content": prompt })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        success, response_data = api_call("post", f"{config.API_URL}/chat", json={
            "provider": st.session_state.provider,
            "model_name": st.session_state.model_name,
            "messages": st.session_state.messages
        })
        
        if success:
            answer = response_data.get("message", "")
        else:
            answer = f"Error: {response_data.get('message') or response_data.get('detail', 'Unknown error')}"
        st.markdown(answer)
    st.session_state.messages.append({ "role": "assistant", "content": answer })
#--------------------------------------------------------------