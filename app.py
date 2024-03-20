import streamlit as st
from openai import OpenAI
from streamlit_option_menu import option_menu

system_instruction_for_chat_model = """
You are a helpful AI assistant meant to help users with supply chain questions.

Introduce yourself to the user as an assistant meant for this task.

Regardless of the user's inquiries, always focus the conversation on supply chain-related topics. 
If the user veers off topic, politely guide them back to the subject matter.

Respond to user queries with concise and informative answers pertaining to supply chain management. 
Avoid irrelevant information or tangents.

Interact with users in a courteous and respectful manner at all times. 
Even when redirecting the conversation, ensure that the tone remains friendly and helpful.
"""
system_instruction_for_pdf_model = """
You are an accurate AI Assistant helping people get the best out of their PDFs.

Introduce yourself to the user for this purpose and ask them to upload a PDF for you to help them with their questions.

Regardless of the user's inquiries, always focus the conversation analyzing the PDF and helping user understand it better. 
If the user veers off topic, politely guide them back to the subject matter.

Interact with users in a courteous and respectful manner at all times. 
Even when redirecting the conversation, ensure that the tone remains friendly and helpful.
"""

st.set_page_config(
    page_title="SCM Chatbot",
    layout="wide",
    page_icon="🤖"
)

with st.sidebar:
    st.markdown("### **💬Welcome onboard!**")
    selected = option_menu(
        menu_title="Current Features",
        options=[
            "SCM Chatbot",
            "PDF Analyzer"
        ],
        icons=[
            'chat-right-dots-fill', 'filetype-pdf'  # https://icons.getbootstrap.com/
        ],
        menu_icon="list-nested",
        default_index=0,
        orientation="vertical"
    )

if selected == "SCM Chatbot":

    st.title("Supply Chain Management")
    st.image("www/img/scm_pic.png")

    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_instruction_for_chat_model}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Hi there! How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

    # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
else:
    st.write("Hi there! I can help you get answers quickly from your PDFs.")
    st.write("Just upload it below and then ask me anything")

    file_from_user = st.file_uploader(
        "Upload PDF",
        accept_multiple_files=False,
        key="uploaded_pdf"
    )

    if file_from_user != None:
        st.write(file_from_user.name)
    # files = [
    #     ('file', ('file', open('www/pdfs/test_pdf.pdf', 'rb'), 'application/octet-stream'))
    # ]

    # Initialize chat history
    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = [
            {"role": "system", "content": ""}
        ]
