import sys, os, time, streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from itertools import cycle
from app.graph import run_graph
from app.chat_db import (
    init_chat_db, create_new_session, list_sessions,
    save_message, load_messages, delete_session, rename_session
)
from app.nodes.utils import call_llm


# ---------------- Init ----------------
init_chat_db()

# ---------------- Page Config ----------------
st.set_page_config(page_title="💬 Sales Data Chatbot", layout="wide")

# ---------------- ChatGPT-like UI Styling ----------------
st.markdown("""
<style>
body {
    background-color: #0e0e10;
    color: #f1f1f1;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #1a1a1d;
    border-right: 1px solid #2d2f3e;
}
.sidebar-title {
    font-weight: 600;
    margin-bottom: 10px;
    color: #ccc;
}
.chat-item {
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 4px;
    color: #eee;
    text-align: left;
}
.chat-item:hover {
    background-color: #2a2a2e;
}
.chat-item.selected {
    background-color: #34343a;
    color: white;
    font-weight: 500;
}
.stButton>button {
    background-color: #2a2a2e;
    border: none;
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
}
.stButton>button:hover {
    background-color: #38383e;
}
</style>
""", unsafe_allow_html=True)

st.title("💬 Chat with Your Sales Data")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Chats</div>', unsafe_allow_html=True)

    sessions = list_sessions()
    selected_session = st.session_state.get("session_id")

    # ✅ “New Chat” button
    if st.button("➕ New Chat", use_container_width=True):
        sid = create_new_session("Untitled Chat")
        st.session_state.session_id = sid
        st.session_state.auto_name_needed = True
        st.rerun()

    st.markdown("---")

    # List existing chats
    for sid, name, _ in sessions:
        class_name = "chat-item selected" if sid == selected_session else "chat-item"
        if st.button(name, key=f"chat_{sid}", use_container_width=True):
            st.session_state.session_id = sid
            st.rerun()

    st.markdown("---")
    st.caption("💡 Chats are saved automatically.")

# ---------------- Main Chat ----------------
session_id = st.session_state.get("session_id")

if not session_id:
    st.info("👈 Click **New Chat** in the sidebar to start your conversation.")
    st.stop()

messages = load_messages(session_id)

# Display chat history
for role, msg in messages:
    with st.chat_message(role):
        st.markdown(msg)

# ---------------- Chat Input ----------------
user_query = st.chat_input("Ask your question about sales data...")

# ---------------- Chat Logic ----------------
if user_query:
    # Save user message
    save_message(session_id, "user", user_query)

    with st.chat_message("user"):
        st.markdown(user_query)

    # Thinking animation (ChatGPT-like)
    thinking = st.empty()
    loader = cycle(["Thinking.", "Thinking..", "Thinking..."])
    for _ in range(4):
        thinking.markdown(f"🧠 {next(loader)}")
        time.sleep(0.5)
    thinking.empty()

    # Stream model response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        try:
            final_response = run_graph(user_query, session_id=session_id)
            for ch in final_response:
                full_text += ch
                placeholder.markdown(full_text + "▌")
                time.sleep(0.01)
            placeholder.markdown(full_text)
            save_message(session_id, "assistant", full_text)

            # ✅ Rename chat automatically if first interaction
            if len(load_messages(session_id)) <= 2:  # 1 user + 1 assistant
                try:
                    rename_prompt = f"Give a short, clear title (<=30 chars) for this chat:\n\nUser: {user_query}\nAssistant: {full_text}"
                    new_name = call_llm(rename_prompt)
                    short_name = new_name.strip().split('\n')[0][:30]
                    rename_session(session_id, short_name)
                except Exception:
                    rename_session(session_id, "Quick Chat")

        except Exception as e:
            err = f"⚠️ Error: {e}"
            placeholder.error(err)
            save_message(session_id, "assistant", err)
