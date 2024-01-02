
Made and Deployed Legal Chatbot Advisor with [Langchain](https://python.langchain.com/docs/get_started/introduction), [Pinecone](https://www.pinecone.io/), [LlamaAPI](https://www.llama-api.com/), [Huggingface Space](https://huggingface.co/spaces/gabruarya/legal-advisor) and [Streamlit](https://docs.streamlit.io/) 

# Legal Chatbot Advisor

Welcome to the Legal Chatbot Advisor project! This chatbot is designed to provide legal advice based on user queries related to the Indian legal system.

## Features

- Quick and automated legal advice
- Utilizes Langchain for natural language processing
- Pinecone for efficient similarity search
- Streamlit for a user-friendly interface

Use chabot yourself at [Huggingface Space](https://huggingface.co/spaces/gabruarya/legal-advisor)  

## Installation

To run the Legal Chatbot Advisor locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/GabruAru/LegalEase-Chatbot-Advisor.git
   ```

2. Navigate to the project directory:

   ```bash
   cd LegalEase-Chatbot-Advisor
   ```
   
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1. Create secrets.toml inside .streamlit folder and update it with.
   ``` bash
   HUGGINGFACEHUB_API_TOKEN = "YOUR_TOKEN"
   PINECONE_API_KEY = "YOUR_PINECONCE_KEY"
   PINECONE_API_ENV = "YOUR_ENV_NAME"
   LlamaAPI = "YOUR_LLAMAAPI_KEY"
   ```

2. Run the Streamlit app:
   
   ```bash
   streamlit run app.py
   ```
3. Open your web browser and go to http://localhost:8501.
   
4. Interact with the Legal Chatbot Advisor by entering your legal questions.
   
