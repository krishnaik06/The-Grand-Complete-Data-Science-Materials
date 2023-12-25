<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>WALMART-SALESBOT-AND-SEARCHGPT</h1>
<h3>◦ SalesBot-SearchGPT: Innovating Sales Agent of Walmart, and Custom Search GPT bot!</h3>
<h5 align="center">Connect with me: <a href="https://www.linkedin.com/in/shaon2221">LinkedIn</a> 🚀</h5>
<h3>◦ Developed with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style=flat-square&logo=tqdm&logoColor=black" alt="tqdm" />
<img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=flat-square&logo=Jupyter&logoColor=white" alt="Jupyter" />
<img src="https://img.shields.io/badge/arXiv-B31B1B.svg?style=flat-square&logo=arXiv&logoColor=white" alt="arXiv" />
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=flat-square&logo=OpenAI&logoColor=white" alt="OpenAI" />

<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat-square&logo=Pytest&logoColor=white" alt="Pytest" />
<img src="https://img.shields.io/badge/Wikipedia-000000.svg?style=flat-square&logo=Wikipedia&logoColor=white" alt="Wikipedia" />
</p>
<img src="https://img.shields.io/github/license/Shaon2221/Walmart-SalesBot-and-SearchGPT?style=flat-square&color=5D6D7E" alt="GitHub license" />
<img src="https://img.shields.io/github/last-commit/Shaon2221/Walmart-SalesBot-and-SearchGPT?style=flat-square&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/Shaon2221/Walmart-SalesBot-and-SearchGPT?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/Shaon2221/Walmart-SalesBot-and-SearchGPT?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

---

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
  - [Walmart Bot](#walmart-bot)
    - [Walmart Bot Functionality](#walmart-bot-functionality)
    - [Technical Implementation](#technical-implementation)
    - [API and Framework Choices](#api-and-framework-choices)
  - [SearchGPT Functionality](#searchgpt-functionality)
    - [Technical Implementation](#technical-implementation-1)
- [📦 Features](#-features)
- [📂 Repository Structure](#-repository-structure)
- [⚙️ Modules](#️-modules)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Installation](#-installation)
  - [🤖 Running Walmart-SalesBot-and-SearchGPT](#-running-walmart-salesbot-and-searchgpt)
  - [🕹️ Running using Docker](#️-running-using-docker)
  - [✨ Interface](#-interface)
- [🛣 Project Screenshots](#-project-screenshots)
- [🤝 Contributing](#-contributing)
    - [*Contributing Guidelines*](#contributing-guidelines)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)
- [🛠️How to deploy the project](#️how-to-deploy-the-project)
- [🧑‍🚀How to contact the Author](#how-to-contact-the-author)

---


## 📍 Overview

The Walmart SalesBot and SearchGPT repository provides a AI solution to improve customer service and search capabilities. The tool includes an AI chatbot, enabling users to interact with either the'WalmartBot' or'SearchGPT' bot in real-time. It utilizes a robust conversational AI agent that can fetch webpage content, gather weather details, conduct searches, and retrieve news. It provides a sales assistance system for Walmart, implementing stages of sales conversations and managing customer interactions. Additionally, the repository includes an API server for product search and information retrieval.This project draws inspiration from SalesGPT and various other open-source initiatives. It is important to note that no direct copying or borrowing of ideas has occurred, and sincere gratitude is extended to all open source projects. 

### Walmart Bot
The Streamlit interface offers users two distinct options: Walmart Bot and SearchGPT.

#### Walmart Bot Functionality
The Walmart Bot functionality allows users to seamlessly search for products on Walmart. Additionally, it provides responses to specific product-related queries such as pricing inquiries and feature comparisons (e.g., "What is the price of iPhone 12?" or "Compare features of products"). Each response is accompanied by a source link or product link, offering users a comprehensive answer.

#### Technical Implementation
- Language Models: OpenAI models are employed in the project, with the flexibility to utilize any open-source model from Hugging Face.
- Langchain: The system leverages Langchain to enhance its functionality. Techniques such as Prompt Engineering, RetrievalQA, and Vector Database utilization contribute to the robustness of the system.
- Vector Database: Pinecone serves as the vector database, providing efficient storage and retrieval capabilities. The system is adaptable, allowing the use of alternative vector databases or traditional databases via llamaindex.
- Embeddings: OpenAI embeddings are utilized in the current implementation, though open-source embeddings can be seamlessly integrated for further customization.
#### API and Framework Choices
- API Framework: FastAPI is chosen to develop the API, providing a high-performance and user-friendly interface. However, the system is designed to be flexible, allowing the use of alternative frameworks like Flask or others.
- User Interface Framework: Streamlit is employed to construct the interface, offering a visually appealing and interactive platform. Users have the freedom to choose alternative frameworks based on their preferences.

### SearchGPT Functionality
In addition to Walmart Bot, the interface also facilitates the use of SearchGPT, enabling users to search for any question and obtain answers from the internet.

#### Technical Implementation
Language Models: Large language models are utilized in combination with LangChain and various tools to power the SearchGPT system.

---

## 📦 Features

|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The system is a conversational agent combining REST APIs, Search and Recommendation systems built with Python. It utilizes Python scripts, Jupyter Notebook, and Docker for deployment.|
| 📄 | **Documentation**  | The repository lacks a comprehensive README.md file, providing a detailed explanation of the system. Absence of inline comments make it hard to understand the modules' purpose.|
| 🔗 | **Dependencies**   | The system extensively relies on external libraries such as Pydantic, FAISS, OpenAI, Pinecone, DuckDuckGo, and much more for operating its functionalities.|
| 🧩 | **Modularity**     | The system is loosely coupled and separated into several scripts, each responsible for handling a certain aspect, making it adaptable, understandable, and maintainable.|
| 🧪 | **Testing**        | The system uses pytest as a testing framework but lacks any presence of dedicated test cases to validate its functionality.   |
| ⚡️ | **Performance**    | The system's performance heavily relies on the  efficiency of GPT AI model & Pinecone search engine, hence can be inferred to be performant. But it lacks performance testing or benchmarking.|
| 🔐 | **Security**       | There aren't any explicit security measures found. The system being API based, needs to ensure critical information is sanitized before processing. |
| 🔀 | **Version Control**| The repository lacks specific version control strategy as there's absence of branches, tags or even comprehensive commit messages. |
| 🔌 | **Integrations**   | The system integrates with various Python libraries, APIs, GPT AI model, and Walmart's product data, supporting the bot functionalities.|
| 📶 | **Scalability**    | The system is scalable due to its loosely coupled design that would support future enhancements, provided there is efficient error handling and architectural improvements. |


---


## 📂 Repository Structure

```sh
└── Walmart-SalesBot-and-SearchGPT/
    ├── Data/
    ├── Dockerfile
    ├── Images/
    ├── csv_to_vectore_database(pinecone).ipynb
    ├── requirements.txt
    ├── run_api.py
    ├── search_capabilities.py
    ├── streamlit_interface.py
    └── walmart_functions.py

```

---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                                                                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [streamlit_interface.py](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/streamlit_interface.py)                                   | The code powers an AI chatbot web application with Streamlit. It allows users to choose between "WalmartBot" and "SearchGPT" bot types and interact with them real-time. It maintains a chat interface, showing recent user-bot conversations applying a dark or light theme based on user preference. Both types of bot responses are handled via POST requests to defined endpoints.                                                                                                                                                                                                                                                                                             |
| [search_capabilities.py](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/search_capabilities.py)                                   | The code implements a conversational AI agent in Python. It integrates third-party tools to fetch webpage content, gather weather details, conduct searches (via DuckDuckGo), and retrieve news. Besides, it specifies a set of behavior rules for the AI. The'get_response' function runs an input message through the AI agent, which interacts with tools based on its training and guidelines, getting necessary data, and returning a response. The system hides detailed error responses from users, replacing them with a generic misunderstanding message.                                                                                                                 |
| [csv_to_vectore_database(pinecone).ipynb](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/csv_to_vectore_database(pinecone).ipynb) | The code represents a part of a Jupyter notebook in the directory Walmart-SalesBot-and-SearchGPT. It attempts to install necessary dependencies such as protobuf, fastapi, uvicorn, langchain, openai, tiktoken, pinecone-client, and pinecone_datasets using pip. However, it encounters an error while attempting to install a specific version of pinecone_datasets.                                                                                                                                                                                                                                                                                                            |
| [run_api.py](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/run_api.py)                                                           | The code comprises an API for a Walmart Sales Bot, which searches for products and returns relevant information, and a Search AI, which fetches answers from sources like DuckDuckGo, Wikipedia, weather API, and Arxiv. The API employs FastAPI and pydantic models for request/response handling. Both services initialize a new conversation if no user inputs are present or continue pre-existing conversations. The bots respond with messages and potential sources of their responses. Errors raise an HTTP Exception.                                                                                                                                                     |
| [walmart_functions.py](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/walmart_functions.py)                                       | This complex Python script implements a sales assistance system for Walmart. The tool leverages OpenAI's GPT-4 model and Natural Language Understanding chains to guide sales conversations through different stages (Introduction, Product presentation, and Other queries) based on conversation history. It integrates with Pinecone to access a vector-based product database, offering product search and information retrieval for shaping responses. A custom class is designed to manage sales conversations, initiating conversations, determining next stages, handling customer input, and generating responses, optionally using a knowledge base for product queries. |
| [Dockerfile](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/Dockerfile)                                                           | The Dockerfile deploys a Python-based app for a Walmart sale-search bot through a Docker environment. It works by installing dependencies from requirements.txt, copying application files into the container, and running the application using the command'run_api.py' on port 5000. Other scripts in the repository appear to implement related functions like data conversion to vector format, search capabilities, and a Streamlit user interface.                                                                                                                                                                                                                           |
| [requirements.txt](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/requirements.txt)                                               | The code sets up a Walmart SalesBot and SearchGPT program that utilizes machine learning and natural language processing for data analysis and search-related capabilities. Dependencies include openai and pytest for testing, faiss-cpu and pinecone-client for vector search indexing, black and flake8 for code formatting, Pydantic for data validation and settings management, and chromadb and xmltodict for handling data. Search results can be enhanced by duckduckgo-search, wikipedia and arxiv. The program includes an API server using uvicorn.                                                                                                                    |

</details>

---

## 🚀 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system: [requirements.txt](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/requirements.txt)

### 🔧 Installation

1. Clone the Walmart-SalesBot-and-SearchGPT repository:
```sh
git clone https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT
```

2. Change to the project directory:
```sh
cd Walmart-SalesBot-and-SearchGPT
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🤖 Running Walmart-SalesBot-and-SearchGPT

```sh
python run_api.py
```
### 🕹️ Running using Docker
```
docker build -t bot .
docker run -p 5000:5000 bot
```

### ✨ Interface
```sh
streamlit run streamlit_interface.py
```

---


## 🛣 Project Screenshots

![Walmart_Bot Screenshot](https://raw.githubusercontent.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/main/Images/walmart_bot-screenshot.png)

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/Shaon2221/Walmart-SalesBot-and-SearchGPT/issues)**: Submit bugs found or log feature requests for Shaon2221.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

## 📄 License


This project is protected under the MIT License.

---

## 👏 Acknowledgments

- This projects is inspired by SalesGPT and other open source projects. But not copy paste, or any idea has not been stolen. Thanks to all the contributors.

## 🛠️How to deploy the project
You can deploy the project using Docker or Streamlit. You can also deploy the project using Heroku, AWS, or any other cloud platform.

## 🧑‍🚀How to contact the Author
You can contact me at: [LinkedIn](https://www.linkedin.com/in/shaon2221)

[**Return**](#Top)

---
