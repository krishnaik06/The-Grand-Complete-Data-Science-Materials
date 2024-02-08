#Streamlit is a free, open-source Python library that helps developers 
#and data scientists create interactive web applications for machine learning 
#and data science
import streamlit as st
from streamlit_chat import message

#ConversationalRetrievalChain is designed to process queries and generate responses by leveraging 
#information extracted from the associated documents. 
#It represents a form of Retrieval-Augmented Generation (RAG), offering a method to 
#enhance the quality of generated responses through retrieved documents.
from langchain.chains import ConversationalRetrievalChain

#Conversational memory is the mechanism that empowers a chatbot to respond 
#coherently to multiple queries, providing a chat-like experience. 
#It ensures continuity in the conversation, allowing the chatbot to consider 
#past interactions and provide contextually relevant responses.
from langchain.memory import ConversationBufferMemory

# All utility functions
import utils

from PIL import Image

def initialize_session_state():
    """
    Session State is a way to share variables between reruns, for each user session.
    """

    st.session_state.setdefault('history', [])
    st.session_state.setdefault('generated', ["Hello! I am here to provide answers to questions extracted from uploaded PDF files."])
    st.session_state.setdefault('past', ["Hello Buddy!"])

def create_conversational_chain(llm, vector_store):
    """
    Creating conversational chain using Mistral 7B LLM instance and vector store instance

    Args:
    - llm: Instance of Mistral 7B GGUF
    - vector_store: Instance of FAISS Vector store having all the PDF document chunks 
    """

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain

def display_chat(conversation_chain):
    """
    Streamlit relatde code wher we are passing conversation_chain instance created earlier
    It creates two containers
    container: To group our chat input form
    reply_container: To group the generated chat response

    Args:
    - conversation_chain: Instance of LangChain ConversationalRetrievalChain
    """
    #In Streamlit, a container is an invisible element that can hold multiple 
    #elements together. The st.container function allows you to group multiple 
    #elements together. For example, you can use a container to insert multiple 
    #elements into your app out of order.
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask me questions from uploaded PDF", key='input')
            submit_button = st.form_submit_button(label='Send ⬆️')
        
        #Check if user submit question with user input and generate response of the question
        if submit_button and user_input:
            generate_response(user_input, conversation_chain)
    
    #Display generated response to streamlit web UI
    display_generated_responses(reply_container)


def generate_response(user_input, conversation_chain):
    """
    Generate LLM response based on the user question by retrieving data from Vector Database
    Also, stores information to streamlit session states 'past' and 'generated' so that it can
    have memory of previous generation for converstational type of chats (Like chatGPT)

    Args
    - user_input(str): User input as a text
    - conversation_chain: Instance of ConversationalRetrievalChain 
    """

    with st.spinner('Spinning a snazzy reply...'):
        output = conversation_chat(user_input, conversation_chain, st.session_state['history'])

    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

def conversation_chat(user_input, conversation_chain, history):
    """
    Returns LLM response after invoking model through conversation_chain

    Args:
    - user_input(str): User input
    - conversation_chain: Instance of ConversationalRetrievalChain
    - history: Previous response history
    returns:
    - result["answer"]: Response generated from LLM
    """
    result = conversation_chain.invoke({"question": user_input, "chat_history": history})
    history.append((user_input, result["answer"]))
    return result["answer"]


def display_generated_responses(reply_container):
    """
    Display generated LLM response to Streamlit Web UI

    Args:
    - reply_container: Streamlit container created at previous step
    """
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=f"{i}_user", avatar_style="adventurer")
                message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")

def main():
    """
    First function to call when we start streamlit app
    """
    # Step 1: Initialize session state
    initialize_session_state()
    
    st.title("Chat Bot")

    image = Image.open('D:\Project\ChatBot\Chatbot.jpg')
    st.image(image, width=150)
    
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>

            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    # Step 2: Initialize Streamlit
    st.sidebar.title("Upload Pdf")
    #file_uploader, the data are copied to the Streamlit backend via the browser, 
    #and contained in a BytesIO buffer in Python memory (i.e. RAM, not disk).
    pdf_files = st.sidebar.file_uploader("", accept_multiple_files=True)
    
    # Step 3: Create instance of Mistral 7B GGUF file format using llama.cpp    
    llm = utils.create_llm()

    #Step 4: Create Vector Store and store uploaded Pdf file to in-mempry Vector Database FAISS
    # and return instance of vector store
    vector_store = utils.create_vector_store(pdf_files)

    if vector_store:
        #Step 5: If Vetor Store created successful with chunks of PDF files
        # then Create the chain object
        chain = create_conversational_chain(llm, vector_store)

        #Step 6 - Display Chat to Web UI
        display_chat(chain)
    else:
        print('Initialzed App.')

if __name__ == "__main__":
    main()
