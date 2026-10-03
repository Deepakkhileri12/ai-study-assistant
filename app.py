import streamlit as st
from UI.dashboard import render_ui
from ai_agent import get_rag_chain, get_answer_from_rag_chain

st.set_page_config(
    page_title="AI Study Assistant",
    layout="wide"
)

@st.cache_resource
def load_rag():
    return get_rag_chain()

rag_chain = load_rag()
render_ui(rag_chain, get_answer_from_rag_chain)