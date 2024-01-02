# DS-AI-Bot-Interviewer
This is an DS AI Interviewer. It helps to prepare for the data science interviews by asking quesions based on user selection perference. It will analyze the user answer and provide feedback and also provide simplified answer to the user. So, user will learn and understand the concept easily and also he knows the mistakes.

#### Clone the git repository
```bash
git clone https://github.com/elavalasrinivasreddy/DS-AI-Bot-Interviewer.git
```
#### Change the directory
```bash
~$ cd
```
#### Create conda environment
```bash
conda create -n AI_Interviewer python=3.9
```
#### Activate the environment and install requirements
```bash
conda activate AI_Interviewer
python -m pip install -r requirements.txt
```
#### For GPU activation run the below commands 
```bash
conda install -c anaconda cudatoolkit
conda install -c anaconda cudnn
Download Pytorch by visiting https://pytorch.org/  {choose pip}
```
#### To check python is accessing cuda {True - We can use GPU}
```bash
import torch
print("torch.cuda.is_available")
```
#### Create a .env in your directory and mention the values for below keys
```bash
MODEL_NAME=
MODEL_FILE=
TOKENIZER =
HF_API=
HF_HOME= 'if you want to change the cache dir'
```
#### To Run the Application
```bash
streamlit run app.py
```
#### Tech-stack
```bash
--Python
--Langchain
--Streamlit
--Meta Llama-2
--HuggingFace Transformers
```
### Sample Web UI snapshot
![final](https://github.com/elavalasrinivasreddy/DS-AI-Bot-Interviewer/assets/45328855/8ee5093b-c122-4d42-a247-d67bb7382f6d)