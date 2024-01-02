import streamlit as st
from PIL import Image
from src.model_load import load_model_LC
from src.helper import Create_LLM_chain
import time

print('==='*20)

# Read the logo png
icon_img = Image.open('png_data\icon.png')
# set the page config
st.set_page_config(page_title = 'AI Bot Interviewer', # page title
                page_icon = icon_img, # logo image
                layout = 'centered', # layout is centered
                initial_sidebar_state = 'auto' # removing the sidebar {By default it will come}
                )
# Set the page Header
st.title('DS Interview By Llama-2 ')

# Load the model
model = load_model_LC()

if "prev_topic" not in st.session_state:
    st.session_state.prev_topic = ""

# if "messages" not in st.session_state:
#     st.session_state.messages = []

def clear_chat():
    if "messages" in st.session_state:
        st.info('Chat History Was Cleared.!', icon="ℹ️")
    st.session_state.messages = []
    print('Chat Was Cleared..!')

# adding optional topics for the user
topic = st.sidebar.radio(
        "Choose Prefered Topic ",
        key="topic",
        index= 0,
        # on_change = clear_chat(),
        horizontal = False,
        options=["All",
                "Statistics",
                "Data Cleaning",
                "Data Preprocessing",
                "Machine Learning",
                "Deep Learning",
                "Large Language Models",
                "Natural Language Processing",
                "Computer Vision",
                ],
    )

# clear chat button 
st.sidebar.button("Clear Chat",key='clear_chat',on_click=clear_chat)

if topic and topic != st.session_state.prev_topic:
    st.session_state.chain_model = Create_LLM_chain(model_obj=model)
    print('New Prompt was generated for ...',st.session_state.topic)
    st.session_state.prev_topic = topic
    clear_chat()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == 'human':
        avatar = "🕵🏻‍♀️"
    else:
        avatar = "🧠"
    with st.chat_message(message["role"],avatar=avatar):
        st.markdown(message["content"])

if prompt:= st.chat_input("Typing..."):
    # display user messages
    with st.chat_message("human",avatar="🕵🏻‍♀️"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "human","content": prompt})

    # response from LLM
    with st.chat_message("ai",avatar="🧠"):
        message_placeholder = st.empty()
        full_response = ""
        # generate response from LLM
        s_t = time.time()
        with st.spinner('Thinking...'):
            response = st.session_state.chain_model.predict(user_input=prompt)
            # response = prompt
        print('Escaped time for response ',time.time()-s_t)
        # simulate stream of response with milli seconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.07)
            # add a blinking  cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "ai", "content": full_response})