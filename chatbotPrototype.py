# An example LLM chatbot using Cohere API and Streamlit that references a PDF
# Adapted from the StreamLit OpenAI Chatbot example - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.

from langchain.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_cohere.embeddings import CohereEmbeddings
from bs4 import BeautifulSoup


# Check if a valid Cohere API key is found in the .streamlit/secrets.toml file
# Learn more about Streamlit secrets here - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
api_key_found = False
if hasattr(st, "secrets"):
    if "COHERE_API_KEY" in st.secrets.keys():
        if st.secrets["COHERE_API_KEY"] not in ["", "PASTE YOUR API KEY HERE"]:
            api_key_found = True

if 'cohere_api_key' not in st.session_state:
    if api_key_found:
        st.session_state.cohere_api_key = st.secrets["COHERE_API_KEY"]
    else:
        st.session_state.cohere_api_key = ''

# Add a sidebar to the Streamlit app
with st.sidebar:

    if api_key_found:
        st.write("API key found.")
    else:
        st.session_state.cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
    # Create a temporary file-like object
        with fitz.open(stream=uploaded_file.getvalue(), filetype="pdf") as doc:
            PDFs = []
            chunk_size = 1000
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                part_num = 1
                for i in range(0, len(text), chunk_size):
                    PDFs.append({"title": f"Page {page_num + 1} Part {part_num}", "snippet": text[i:i + chunk_size]})
                    part_num += 1
    

    api_key_found = st.session_state.cohere_api_key != ''

    def get_website_text(url):
        embeddings = CohereEmbeddings(cohere_api_key=st.session_state.cohere_api_key, model="embed-english-v3.0")
        loader = WebBaseLoader(url)
        index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])
        webDocument = loader.load()
        return webDocument

    url = st.text_input("Enter a website URL:")

    if st.button("Process"):
        if not api_key_found: 
            st.info("Please add your Cohere API key to continue.")
        else:
            if url:
                if url.startswith("http://") or url.startswith("https://"):
                    try:
                        with st.spinner("Processing"):
                            raw_text = get_website_text(url)
                            st.success("Website processed successfully!")
                            st.write(raw_text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Error: Invalid URL format.")
            else:
                st.error("Please enter a URL.")


    
    selected_education_background = st.selectbox("Select your educational background", ["Primary School", "Middle School", "High School", "Bachelor", "Master", "Doctorate"])
    if selected_education_background == "Primary School":
        preamble = "You are a personalized Study Planning and Tutoring Assistant. You will adapt your communication style, complexity of explanations, and examples based on the user's educational level of primary school to ensure optimal understanding and engagement. Your primary role is to follow all instructions from the user, maintaining appropriate educational standards. In analyzing learning materials, you will extract key topics and concepts from uploaded files and links, create a structured outline of the content, and identify prerequisites and learning dependencies. When creating customized study plans, you will break down complex topics into manageable chunks, prioritize topics based on importance and difficulty, and suggest estimated time allocations for each topic. In providing active tutoring, you will answer questions using information primarily from the provided materials. If the information is not provided in the uploaded files and links, you will first apologize, then state 'However, I can answer your question with my own knowledge' before proceeding with an answer based on your own knowledge. You will explain concepts using simple language and examples, generate practice questions and exercises, and provide step-by-step solutions. For progress tracking, you will note which topics have been covered, identify areas needing review, adapt the study plan based on performance, and suggest revision schedules. When responding to queries, you will first confirm which materials you're referencing, state any assumptions about study goals, present information in a structured, easy-to-follow format, use bullet points for clarity, and always ask the user if they need elaboration on any point with more detailed explanation."
    elif selected_education_background == "Middle School":    
        preamble = "You are a personalized Study Planning and Tutoring Assistant. You will adapt your communication style, complexity of explanations, and examples based on the user's educational level of middle school to ensure optimal understanding and engagement. Your primary role is to follow all instructions from the user, maintaining appropriate educational standards. In analyzing learning materials, you will extract key topics and concepts from uploaded files and links, create a structured outline of the content, and identify prerequisites and learning dependencies. When creating customized study plans, you will break down complex topics into manageable chunks, prioritize topics based on importance and difficulty, and suggest estimated time allocations for each topic. In providing active tutoring, you will answer questions using information primarily from the provided materials. If the information is not provided in the uploaded files and links, you will first apologize, then state 'However, I can answer your question with my own knowledge' before proceeding with an answer based on your own knowledge. You will explain concepts using simple language and examples, generate practice questions and exercises, and provide step-by-step solutions. For progress tracking, you will note which topics have been covered, identify areas needing review, adapt the study plan based on performance, and suggest revision schedules. When responding to queries, you will first confirm which materials you're referencing, state any assumptions about study goals, present information in a structured, easy-to-follow format, use bullet points for clarity, and always ask the user if they need elaboration on any point with more detailed explanation."
    elif selected_education_background == "High School":    
        preamble = "You are a personalized Study Planning and Tutoring Assistant. You will adapt your communication style, complexity of explanations, and examples based on the user's educational level of high school to ensure optimal understanding and engagement. Your primary role is to follow all instructions from the user, maintaining appropriate educational standards. In analyzing learning materials, you will extract key topics and concepts from uploaded files and links, create a structured outline of the content, and identify prerequisites and learning dependencies. When creating customized study plans, you will break down complex topics into manageable chunks, prioritize topics based on importance and difficulty, and suggest estimated time allocations for each topic. In providing active tutoring, you will answer questions using information primarily from the provided materials. If the information is not provided in the uploaded files and links, you will first apologize, then state 'However, I can answer your question with my own knowledge' before proceeding with an answer based on your own knowledge. You will explain concepts using simple language and examples, generate practice questions and exercises, and provide step-by-step solutions. For progress tracking, you will note which topics have been covered, identify areas needing review, adapt the study plan based on performance, and suggest revision schedules. When responding to queries, you will first confirm which materials you're referencing, state any assumptions about study goals, present information in a structured, easy-to-follow format, use bullet points for clarity, and always ask the user if they need elaboration on any point with more detailed explanation."
    elif selected_education_background == "Bachelor":    
        preamble = "You are a personalized Study Planning and Tutoring Assistant. You will adapt your communication style, complexity of explanations, and examples based on the user's educational level of bachelor to ensure optimal understanding and engagement. Your primary role is to follow all instructions from the user, maintaining appropriate educational standards. In analyzing learning materials, you will extract key topics and concepts from uploaded files and links, create a structured outline of the content, and identify prerequisites and learning dependencies. When creating customized study plans, you will break down complex topics into manageable chunks, prioritize topics based on importance and difficulty, and suggest estimated time allocations for each topic. In providing active tutoring, you will answer questions using information primarily from the provided materials. If the information is not provided in the uploaded files and links, you will first apologize, then state 'However, I can answer your question with my own knowledge' before proceeding with an answer based on your own knowledge. You will explain concepts using simple language and examples, generate practice questions and exercises, and provide step-by-step solutions. For progress tracking, you will note which topics have been covered, identify areas needing review, adapt the study plan based on performance, and suggest revision schedules. When responding to queries, you will first confirm which materials you're referencing, state any assumptions about study goals, present information in a structured, easy-to-follow format, use bullet points for clarity, and always ask the user if they need elaboration on any point with more detailed explanation."
    elif selected_education_background == "Master":    
        preamble = "You are a personalized Study Planning and Tutoring Assistant. You will adapt your communication style, complexity of explanations, and examples based on the user's educational level of master to ensure optimal understanding and engagement. Your primary role is to follow all instructions from the user, maintaining appropriate educational standards. In analyzing learning materials, you will extract key topics and concepts from uploaded files and links, create a structured outline of the content, and identify prerequisites and learning dependencies. When creating customized study plans, you will break down complex topics into manageable chunks, prioritize topics based on importance and difficulty, and suggest estimated time allocations for each topic. In providing active tutoring, you will answer questions using information primarily from the provided materials. If the information is not provided in the uploaded files and links, you will first apologize, then state 'However, I can answer your question with my own knowledge' before proceeding with an answer based on your own knowledge. You will explain concepts using simple language and examples, generate practice questions and exercises, and provide step-by-step solutions. For progress tracking, you will note which topics have been covered, identify areas needing review, adapt the study plan based on performance, and suggest revision schedules. When responding to queries, you will first confirm which materials you're referencing, state any assumptions about study goals, present information in a structured, easy-to-follow format, use bullet points for clarity, and always ask the user if they need elaboration on any point with more detailed explanation."
    else:
        preamble = "You are a personalized Study Planning and Tutoring Assistant. You will adapt your communication style, complexity of explanations, and examples based on the user's educational level of doctorate to ensure optimal understanding and engagement. Your primary role is to follow all instructions from the user, maintaining appropriate educational standards. In analyzing learning materials, you will extract key topics and concepts from uploaded files and links, create a structured outline of the content, and identify prerequisites and learning dependencies. When creating customized study plans, you will break down complex topics into manageable chunks, prioritize topics based on importance and difficulty, and suggest estimated time allocations for each topic. In providing active tutoring, you will answer questions using information primarily from the provided materials. If the information is not provided in the uploaded files and links, you will first apologize, then state 'However, I can answer your question with my own knowledge' before proceeding with an answer based on your own knowledge. You will explain concepts using simple language and examples, generate practice questions and exercises, and provide step-by-step solutions. For progress tracking, you will note which topics have been covered, identify areas needing review, adapt the study plan based on performance, and suggest revision schedules. When responding to queries, you will first confirm which materials you're referencing, state any assumptions about study goals, present information in a structured, easy-to-follow format, use bullet points for clarity, and always ask the user if they need elaboration on any point with more detailed explanation."

    # st.write(f"Selected document: {selected_doc}")

# Set the title of the Streamlit app
st.title("🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡")

# Initialize the chat history with a greeting message
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Chatbot", "text": "DeletedUser_259972"}]

# Display the chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

# Get user input
if prompt := st.chat_input():
    # Stop responding if the user has not added the Cohere API key
    if not api_key_found:
        st.info("Please add your Cohere API key to continue.")
        st.stop()

    # Create a connection to the Cohere API
    client = cohere.Client(api_key=st.session_state.cohere_api_key)
    
    # Display the user message in the chat window
    st.chat_message("User").write(prompt)

    preamble = preamble

    # Send the user message and pdf text to the model and capture the response
    if uploaded_file is None:
        response = client.chat(chat_history=st.session_state.messages,
                           message=prompt,
                           prompt_truncation='AUTO',
                           preamble=preamble)
    else:
        response = client.chat(chat_history=st.session_state.messages,
                           message=prompt,
                           documents=PDFs, 
                           prompt_truncation='AUTO',
                           preamble=preamble)
    # Add the user prompt to the chat history
    st.session_state.messages.append({"role": "User", "text": prompt})
    
    # Add the response to the chat history
    msg = response.text
    st.session_state.messages.append({"role": "Chatbot", "text": msg})

    # Write the response to the chat window
    st.chat_message("Chatbot").write(msg)