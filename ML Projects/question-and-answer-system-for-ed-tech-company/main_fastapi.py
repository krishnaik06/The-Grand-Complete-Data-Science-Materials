from chain_retriever import *
from utils import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome": "to the Codebasics FAQs API"}


@app.post("/retrieve-qa")
def retrieve_qa(querybody: QueryBody):
    # Use the QA retriever to get the QA chain
    qa_chain = qa_retriever.get_qa_chain(
        temperature=querybody.temperature,
        max_output_tokens=querybody.max_output_tokens,
    )
    # You might need to adapt this part to how you want to use the qa_chain
    response = qa_chain(querybody.query)
    return {"response": response}
