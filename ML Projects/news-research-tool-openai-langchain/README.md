# News Research Tool using OpenAI API, Langchain, FAISS and Streamlit

## Problem Statement

Research Analysts currently face challenges in efficiently conducting news research due to the vast amount of information available and the lack of streamlined tools. There is a need for a comprehensive News Research. This is enabled with the use of LLM models from either OpenAI / HuggingFace, Langchain, Faiss - acts as vector database, and Streamlit - to provide UI libraries in Python to enhance the research process and improve efficiency.

## Topics Covered

- Loaders - TextLoader, UnstructuredURLLoader
- Text Splitters
- FAISS - Index and Vector Database
- Retrieval (RetrievalQAWithSourcesChain)
- Streamlit UI and Project Coding

Please go through the notebooks in the research folder to know how the above features are implemented.

## Running the app

1. Install the requirements - `pip install -r requirements.txt`
2. Store your OpenAI API Key in .env file which is to be located in the root folder of this project. It should be in the following format.

```
OPENAI_API_KEY=YOUR-OPENAI-API-KEY
```

3. Run the app - `streamlit run main.py`

## The Application

![News Research Tool](https://github.com/di37/news-research-tool/blob/main/data/screenshots/UI_Screenshot.png?raw=true)

# Resources

1. Special thanks to Mr.Dhaval to create end to end project: https://www.youtube.com/watch?v=MoqgmWV1fm8&ab_channel=codebasics
2. Langchain Documentation: https://python.langchain.com/docs
3. Streamlit Documentation: https://docs.streamlit.io
