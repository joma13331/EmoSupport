# EmoSupport

EmoSupport is a project that uses Langchain to store documents related to anxiety and depression into a vector store. When a question related to these topics is asked, the project uses the vector store to obtain the context and makes an API call to the OpenAI GPT model. Questions are asked by voice and the answer is also obtained as audio. The project uses Whisper from OpenAI to convert speech to text and the TTS library from Coqui for text to speech.

The front-end allows the user to upload additional documents needed for the vector store. A FAISS vector store with some relevant documents regarding anxiety and depression are already present in the project.


The interaction with Emosupport is done in a conversational manner with the bot retaining information about the previous questions. 

# Installation
1. Clone the repository
2. Create a text file names openai_ai_key.txt in the root directory of the project. This file should contain your OpenAI API key.
3. Create a virtual environment and install the requirements mentioned in requirements.txt.
4. Run the following command from the root directory of the project to start the streamlit app:
```
streamlit run StreamlitApp/app.py
```
5. If you want to use ElasticSearch and it is not installed on your system, you can install it using docker. Run the following command to install ElasticSearch:
```
docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.8.0
```


License
This project is licensed under the MIT License - see the LICENSE file for details.

## References

1. [LangChain](https://python.langchain.com)
2. [Streamlit](https://streamlit.io)
3. [OpenAI API](https://beta.openai.com)
4. [Vector Stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
5. [Vector store-backed retriever](https://python.langchain.com/docs/modules/data_connection/retrievers/how_to/vectorstore)
6. [Chain Types](https://python.langchain.com/docs/modules/chains/document/)
7. [Conversation buffer memory](https://python.langchain.com/docs/modules/memory/how_to/buffer)
8. [Conversational Retrieval QA](https://python.langchain.com/docs/modules/chains/popular/chat_vector_db)
9. [Whisper](https://pypi.org/project/openai-whisper/)
10 [Coqui TTS](https://pypi.org/project/TTS/)

