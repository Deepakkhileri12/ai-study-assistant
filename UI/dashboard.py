import os
import time
import base64
import streamlit as st

def render_ui(rag_chain, get_answer_func):
    
    icon_path = "Assest/folder.png"
    icon_base64 = ""
    if os.path.exists(icon_path):
        with open(icon_path, "rb") as f:
            icon_base64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        /* =============================================
           FIXED BOTTOM-RIGHT UPLOADER
           ============================================= */
        div[data-testid="stFileUploader"] {{
            position: fixed !important;
            right: 35px !important;
            bottom: 25px !important;
            width: 170px !important;
            z-index: 999999 !important;
        }}

        /* =============================================
           GREEN PILL CONTAINER
           ============================================= */
        div[data-testid="stFileUploader"] section {{
            background: #70E88B !important;
            border: none !important;
            border-radius: 55px !important;
            height: 65px !important;
            width: 150px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: none !important;
            cursor: pointer !important;
        }}

        /* =============================================
           REMOVE DEFAULT BACKGROUND & BORDERS
           ============================================= */
        div[data-testid="stFileUploader"] > div {{
            background: transparent !important;
            border: none !important;
        }}

        /* =============================================
           HIDE ALL DEFAULT TEXT & ICONS (Cloud, Drag/Drop)
           ============================================= */
        div[data-testid="stFileUploader"] small,
        div[data-testid="stFileUploader"] span,
        div[data-testid="stFileUploader"] svg,
        div[data-testid="stFileUploader"] p {{
            display: none !important;
        }}

        /* =============================================
           UPLOAD BUTTON OVERLAY
           ============================================= */
        div[data-testid="stFileUploader"] button {{
            background: transparent !important;
            border: none !important;
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            font-size: 0 !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        /* =============================================
           CUSTOM ICON (From Base64)
           ============================================= */
        div[data-testid="stFileUploader"] button::before {{
            content: "";
            display: inline-block;
            width: 22px;
            height: 22px;
            margin-right: 13px;
            vertical-align: middle;
            background-image: url("data:image/png;base64,{icon_base64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}

        /* =============================================
           CUSTOM TEXT ("Add PDF")
           ============================================= */
        div[data-testid="stFileUploader"] button::after {{
            content: "Add PDF";
            font-size: 15px;
            font-weight: 500;
            color: #175A27;
            vertical-align: middle;
        }}

        /* =============================================
           HOVER EFFECT
           ============================================= */
        div[data-testid="stFileUploader"] section:hover {{
            background: #62DC7E !important;
        }}

        /* =============================================
           UPLOADED FILE CHIP PLACEMENT
           ============================================= */
        div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {{
            position: absolute !important;
            bottom: 115px !important;
            right: 0 !importants;
            width: 260px !important;
        }}

        /* Hide Streamlit Enter Instructions */
        div[data-testid="InputInstructions"] {{
            display: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("AI Study Assistant (Context-Aware Doubt Solver)")

    st.write(
        "Welcome to the AI Study Assistant! This application is designed "
        "to help you solve your doubts and answer questions related to your "
        "studies. You can ask questions, and the AI will provide "
        "context-aware answers to assist you in your learning journey."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None

    with st.form(key="query_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            user_text = st.text_input(
                "Label",
                label_visibility="collapsed",
                placeholder="Ask your question here...",
            )

        with col2:
            submit_btn = st.form_submit_button("Submit", use_container_width=True)

    if submit_btn and user_text:
        with st.spinner("AI is thinking..."):
            answer = get_answer_func(user_text, rag_chain)
            st.session_state.messages.append({"question": user_text, "answer": answer})
        st.rerun()

    for chat in st.session_state.messages:
        st.markdown(f"**Q:** {chat['question']}")
        f"**A:** {chat['answer']}"
        st.markdown(f"**A:** {chat['answer']}")
        st.markdown("---")

    uploaded_file = st.file_uploader(
        "Add PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        if uploaded_file.name != st.session_state.last_uploaded_file:
            st.session_state.last_uploaded_file = uploaded_file.name
            
            pdf_bytes = uploaded_file.getvalue()
            name, ext = os.path.splitext(uploaded_file.name)
            file_name = f"{name}_{int(time.time())}{ext}"

            if not os.path.exists("uploaded_pdfs"):
                os.makedirs("uploaded_pdfs")

            file_path = os.path.join("uploaded_pdfs", file_name)
            with open(file_path, "wb") as f:
                f.write(pdf_bytes)
                
            st.success(f"Saved: {uploaded_file.name}")
            st.cache_resource.clear()
            st.rerun()