import streamlit as st
from openai import OpenAI
from core.config import config



def run_llm(provider, model_name, messages, reasoning_effort="minimal", max_tkens=500):
    if provider == "openai":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tkens,
            reasoning_effort=reasoning_effort
        )
        return response.choices[0].message.content

with st.sidebar:
    st.title("Settings")
    provider = st.selectbox("Select LLM Provider", ["openai"])
    model_name = st.selectbox("Model Name", ["gpt-5-nano", "gpt-5-mini"])
    reasoning_effort = st.selectbox("Reasoning Effort", ["minimal", "moderate", "high"])
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=2000, value=500)

    st.session_state.provider = provider
    st.session_state.model_name = model_name

if "messages" not in st.session_state:
    st.session_state.messages = [{ "role": "assistant", "content": "Hello! How can I assist you today?" }]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({ "role": "user", "content": prompt })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = run_llm(provider, model_name, st.session_state.messages, reasoning_effort, max_tokens)
        response_data = output
        answer = response_data
        st.write(answer)
    st.session_state.messages.append({ "role": "assistant", "content": answer })