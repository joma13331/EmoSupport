"""
This python file will create a web app using streamlit. The app will sattisfy the following requirements:
1. There will be a sidebar with the following options:
    a. A Home Page
    b. A web page to upload documents and create a vector store out of them
    c. A web page to ask questions and get answers from the vector store
    d. A web page to ask questions and get answers from the vector store using a conversational approach

2. The web page to upload documents will have the following options:
    a. A file uploader to upload documents
    b. An input box to enter chunk size
    c. a dropdown to select the type of vector store
    d. A button to create the vector store

3. The web page to ask questions will have the following options:
    a. An input box to enter the number of relevant text to consider for the answer
    b. An audio recorder to record the question
    c. A button to select whether sources should be returned
    d. A radio button to select which core chains for working with Documents  
    e. A audio element to play the answer   

4. The Home Page will have the following information:
    a. A brief description of the project
    
"""

import os
import streamlit as st
from audiorecorder import audiorecorder
from Utils.AudioUtils import AudioUtils
from Utils.ChatGPTLLMUtils import ChatGPTLLMUtils

# Setting the title of the web app
st.title("EmoSupport - Mental Health Chatbot")

# Setting the sidebar
st.sidebar.title("Navigation")
options = ["Home", "Upload Documents", "Ask Questions"]
selected_option = st.sidebar.selectbox("Select an option", options)

# Setting the main page
if selected_option == "Home":

    # A Subheader for the home page
    st.subheader("Welcome to EmoSupport - Mental Health Chatbot")

    # A brief description of the project
    st.write("This Web application is a part of the EmoSupport project. The goal of this project is to create a chatbot that can help people with their mental health issues. This web app is a part of the project that will be used to interact with the chatbot.")
    st.write("You can upload documents relevant for Mental Health and ask questions to the chatbot. The chatbot will answer your questions based on the documents you have uploaded.")

    # Describe the different options available in the sidebar
    st.write("You can use the sidebar to navigate to different pages of the web app. The sidebar has the following options:")
    st.write("1. Home: This page. It contains a brief description of the project.")
    st.write("2. Upload Documents: This page will allow you to upload documents relevant for Mental Health. You can also create a vector store out of the documents you upload.")
    st.write("3. Ask Questions: This page will allow you to ask questions to the chatbot. You can also select the number of relevant text to consider for the answer. You can also select whether sources should be returned. You can also select which core chains for working with Documents. You can also play the answer.")

elif selected_option == "Upload Documents":

    # A subheader for the upload documents page
    st.subheader("Upload Documents")

    # A file uploader to upload documents
    st.write("You can upload documents relevant for Mental Health here. You can upload multiple documents at once.")
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

    # An input box to enter chunk size
    st.write("You can enter the chunk size here. The chunk size is the number of words in each chunk. The default value is 250.")
    chunk_size = st.number_input("Enter the chunk size", value=512, min_value=1, max_value=1024, step=1)

    # a dropdown to select the type of vector store
    st.write("Select the type of vector store you want to create.")
    vector_store_type = st.selectbox("Select the type of vector store", ["FAISS", "ElasticVectorSearch"])


    # A button to create the vector store
    st.write("Click the button below to create the vector store.")
    create_vector_store = st.button("Create Vector Store")

    # If the user clicks the create vector store button
    if create_vector_store:
        # If the user has not uploaded any files
        if uploaded_files is None:
            st.write("Please upload some files.")
        # If the user has uploaded some files
        else:
            # Create a folder to store the uploaded files
            folder_path = "./Docs/Text/"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
            # Save the uploaded files in the folder
            for uploaded_file in uploaded_files:
                with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            # Create a vector store out of the uploaded files
            ChatGPTLLMUtils().store_data_in_vector_store(chunk_size=chunk_size, vector_store_type=vector_store_type)
            st.write("Vector store created successfully.")

elif selected_option == "Ask Questions":

    # A subheader for the ask questions page
    st.subheader("Ask Questions")

    # A radio button to select whether to use previous context
    st.write("Select whether you want to use previous context.")
    use_previous_context = st.radio("Select whether you want to use previous context", ["Yes", "No"])

    if use_previous_context == "No":
        st.session_state.chatgpt_utils = ChatGPTLLMUtils()

    # Creating a session state to store the utils
    if st.session_state.get("chatgpt_utils", None) is None:
        st.session_state.chatgpt_utils = ChatGPTLLMUtils()

    # a dropdown to select the type of vector store
    st.write("Select the vector store you want to access.")
    vector_store_type = st.selectbox("Select the vector store you want to access.", ["FAISS", "ElasticVectorSearch"])

    # An input box to enter the number of relevant text to consider for the answer
    st.write("Enter the number of relevant text to consider for the answer.")
    num_relevant_text = st.number_input("Enter the number of relevant text", min_value=1, max_value=20, value=5, step=1)

    # An input box to enter the minimum score to consider for the answer
    st.write("Enter the minimum score to consider for the answer.")
    min_score = st.number_input("Enter the minimum score", min_value=0.0, max_value=1.0, value=0.1, step=0.1)

    # A radio button to select which core chains for working with Documents
    st.write("Select which core chains for working with Documents.")
    core_chains = st.radio("Select which core chains for working with Documents", ["stuff", "refine", "map_reduce", "map_rerank"])
    
    # An audio recorder to record the question
    st.write("You can record the question here.")
    audio = audiorecorder("Click to record", "Recording...")

    if len(audio)>0:
        print(len(audio))    
        # Save the recorded audio
        os.makedirs("Data/Audio/", exist_ok=True)
        with open("Data/Audio/question.mp3", "wb") as wav_file:
            wav_file.write(audio.tobytes())

        if os.path.exists("Data/Audio/question.mp3"):
            
            # Convert the recorded audio to text
            audio_utils = AudioUtils()
            question = audio_utils.speech_to_text("Data/Audio/question.mp3")

            # A button to ask the question
            st.write("Click the button below to ask the question.")
            ask_question = st.button("Ask Question")

            # If the user clicks the ask question button
            if ask_question:
                # If the user has not created a vector store
                if not os.path.exists(f"{vector_store_type}_index") and vector_store_type == "FAISS":
                    st.write("Please create a vector store first.")
                # If the user has created a vector store
                else:
                    # Ask the question
                    response = st.session_state.chatgpt_utils.ask_question(query=question, num_relevant_text=num_relevant_text, 
                                                        return_sources=False, core_chains=core_chains,
                                                        vector_store_type=vector_store_type, min_score=min_score)
                    # Print the response in a text box
                    st.write(response['answer'])

                    # convert the answer to audio
                    audio_utils.text_to_speech(text=response['answer'], output_path="Data/Audio/answer.wav")

                    # play the answer
                    st.audio("Data/Audio/answer.wav")





             
