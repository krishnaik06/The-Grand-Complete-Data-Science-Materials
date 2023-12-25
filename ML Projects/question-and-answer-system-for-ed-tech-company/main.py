from chain_retriever import *

if __name__ == "__main__":
    qa_chain = qa_retriever.get_qa_chain()
    print(qa_chain("Which courses do you offer?"))
