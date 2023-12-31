from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline,GenerationConfig
from langchain.llms import HuggingFacePipeline
from dotenv import load_dotenv
import streamlit as st
import os

# loading .env
load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_FILE = os.getenv('MODEL_FILE')
os.environ['HF_HOME'] = os.getenv('HF_HOME')

@st.cache_resource(show_spinner='Model Loading...')
def load_model_LC():
    print('Model function is called...')
    # Loading the tokenzier
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,use_fast=True)

    # Loading the LLM model from HF or .cache directory
    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME,
                                                    revision=MODEL_FILE,
                                                    device_map='auto'
                                                    )

    # Creating general configuration
    generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
    generation_config.max_new_tokens = 512
    generation_config.temperature = 0.47
    generation_config.remove_invalid_values = True
    generation_config.do_sample = True

    # Creating the pipeline
    model_pipe = pipeline(task='text-generation',
                        model=base_model,
                        tokenizer=tokenizer,
                        generation_config=generation_config,
                        device_map='auto'
                        )

    # Intergarting the Model into Langchain
    LC_model = HuggingFacePipeline(pipeline=model_pipe,
                                    model_kwargs={'temperature':0.47,
                                                'max_new_tokens':512,
                                                }
                                )
    del base_model,tokenizer,model_pipe
    return LC_model
