import os, json, requests, streamlit as st

st.set_page_config(page_title="Nova", page_icon="✨")

PERSONA = ("You are Nova, a warm, witty assistant. Street-smart, short casual "
           "replies like texting, genuinely helpful, never long-winded unless asked.")

def groq_reply(messages):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={"model": "llama-3.3-70b-versatile", "messages": messages},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

name = st.text_input("what should nova call you?", value=st.session_state.get("name", ""))
if name: st.session_state["name"] = name

if "history" not in st.session_state:
    st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]): st.write(m["content"])

prompt = st.chat_input("say something to nova...")
if prompt:
    st.session_state.history.append({"role": "user", "content": f"{name or 'friend'} says: {prompt}"})
    with st.chat_message("user"): st.write(prompt)
    msgs = [{"role": "system", "content": PERSONA}] + st.session_state.history[-20:]
    reply = groq_reply(msgs)
    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"): st.write(reply)
