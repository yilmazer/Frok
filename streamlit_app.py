from openai import OpenAI
import streamlit as st

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["openrouter_api_key"],
)

st.header("Deep GPT ⚡︎")
st.divider()

if "messages" not in st.ses®sion_sta®te:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "3-4 cümle halinde doğrudan özetle.",
        }
    ]

if prompt := st.chat_input("Mesajınızı Giriniz"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    # Trim to last 5 messages
    trimmed_messages = st.session_state.messages[-5:]
    response = client.chat.completions.create(
        model="qwen/qwen3-14b:free",
        messages=trimmed_messages,
        max_tokens=100,
        stream=True,
    )
    response_content = ""
    for chunk in response:
        if content := chunk.choices[0].delta.content:
            with st.chat_message("assistant"):
                st.markdown(content, end="")
            response_content += content
    st.session_state.messages.append({"role": "assistant", "content": response_content})
