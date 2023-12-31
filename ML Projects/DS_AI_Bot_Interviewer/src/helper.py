import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from src.prompt_maker import *

def Create_LLM_chain(model_obj):

    print('LLM chain Function is called...')

    new_prompt = get_prompt(user_topic=st.session_state.topic,
                            instruction=instruction,
                            system_prompt=system_prompt
                            )
    # print('\n\n',new_prompt)
    # st.write(new_prompt)
    prompt = PromptTemplate(input_variables=["chat_history", "user_input"],
                            template=new_prompt
                            )
    # Creating the memory
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=False)
    # preparing the model to act as AI Assistance using langchain
    LLM_model = LLMChain(llm=model_obj,
                         prompt=prompt,
                         verbose=True, # if its true it will print the history for each new conversion in terminal
                         memory=memory
                        )

    return LLM_model