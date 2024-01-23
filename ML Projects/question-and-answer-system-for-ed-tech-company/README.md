# Question And Answering System using LangChain, Google Palm, FAISS and FastAPI for E-Learning Company

We will be creating Question and Answering System using LangChain, Google palm, FAISS and FastAPI for E-Learning Company based on CSV file that includes FAQs of Codebasics - an E-Learning Company.

## Getting the API Key for using Google Palm

1 - Go the following site:

```
https://makersuite.google.com/app/apikey
```

2 - Create API Key in new project or use existing one. Save it in .env file.

## Getting started with the project

1 - Download dataset to the data folder:

```
wget https://raw.githubusercontent.com/codebasics/langchain/main/3_project_codebasics_q_and_a/codebasics_faqs.csv -O data/codebasics_faqs.csv
```

2 - Install requirements:

```
pip install -r requirements.txt
```

3 - Go through the notebook - `experiments_and_trials.ipynb` under `research` folder to get used to the libraries.

4 - Run the following command to start the server:

```
uvicorn main_fastapi:app --reload
```

5 - Now we can test it on Postman. If it answers questions related to given dataset, it will be good. Otherwise, we will need to check the prompt template defined in `constants.py` under 'utils' folder.

Sample test - if questions answer is not there in the CSV file:
![Test 1](https://github.com/di37/langchain-palm-in-ed-tech/blob/main/screenshots/Screenshot_1.png?raw=true)

If answer to the question is present in the CSV file:
![Test 2](https://github.com/di37/langchain-palm-in-ed-tech/blob/main/screenshots/Screenshot_2.png?raw=true)

7 - To shutdown the server - CTRL + C.

## References

1. Special thanks to Mr.Dhaval to create end to end project: https://www.youtube.com/watch?v=AjQPRomyd-k
2. Langchain Documentation: https://python.langchain.com/docs
3. FastAPI Documentation: https://fastapi.tiangolo.com
