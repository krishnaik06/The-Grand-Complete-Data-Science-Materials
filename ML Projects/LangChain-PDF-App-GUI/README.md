# Langchain-PDF-App-GUI

## Project Description: 

The project aims to develop a PDF querying system that leverages LangChain, a powerful language processing tool, to extract information from PDF documents. By employing LangChain's advanced natural language understanding capabilities, the system will enable users to perform complex searches and obtain specific data points from PDF files efficiently and accurately.

## Website
https://github.com/praj2408/Langchain-PDF-App-GUI/assets/70437673/6f1f0806-f6d5-416d-9f6a-5c5282db2769


## Features:
1. PDF Parsing: The system will incorporate a PDF parsing module to extract text content from PDF files. It will handle various PDF formats, including scanned documents that have been OCR-processed, ensuring comprehensive data retrieval.

2. LangChain Integration: LangChain, a state-of-the-art language processing tool, will be integrated into the system. It will utilize advanced techniques such as natural language understanding, entity recognition, and contextual understanding to process the extracted text from PDFs.

3. Query Generation: The system will provide a user-friendly interface to input search queries. Users can utilize a wide range of search parameters, including keywords, phrases, date ranges, and specific document sections, to formulate complex queries.

4. Natural Language Processing: LangChain will process the user queries using natural language processing techniques. It will identify the relevant context and entities mentioned in the queries and analyze the PDF content accordingly.

5. Search and Retrieval: The system will employ LangChain's processed data to perform intelligent searches within the PDF documents. It will identify and rank the most relevant sections or pages that match the user's query, presenting them in an organized manner for easy retrieval.

6. Data Extraction: In addition to search results, the system will offer the ability to extract specific data points from the PDF documents. Users can define extraction rules based on patterns, keywords, or predefined templates to obtain structured data from unstructured PDF content.

7. User-Friendly Interface: The system will provide a user-friendly web-based interface, enabling users to interact with the PDF querying system seamlessly. It will include features like search history, saved queries, and personalized settings for enhanced usability.


## Potential Use Cases:

1. Legal Research: Lawyers and legal professionals can utilize the system to search for specific legal terms, case references, or precedent information within PDF documents, streamlining their research process.

2. Financial Analysis: Financial analysts can extract relevant data points from financial reports or annual statements stored in PDF format, allowing them to perform comprehensive analysis and generate insights efficiently.

3. Academic Research: Researchers and scholars can utilize the system to search for relevant literature, extract citations, or gather information from academic papers saved as PDFs, simplifying the literature review process.

4. Document Management: Organizations can use the system to organize and search through their extensive PDF document repositories, facilitating efficient document retrieval and reducing manual effort.

## Model Information
Generative Pre-trained Transformer 3.5 (GPT-3.5) is a sub class of GPT-3 Models created by OpenAI in 2022.

You can use different models depending on the cost:

 - gpt-3.5-turbo
 - gpt-3.5-turbo-0301
 - gpt-3.5-turbo-0613
 - gpt-3.5-turbo-16k
 - gpt-3.5-turbo-16k-0613


## Conclusion:

By leveraging LangChain's powerful language processing capabilities, the PDF querying system described above aims to enhance the efficiency and accuracy of extracting information from PDF documents. It will empower users across various domains to perform complex searches, extract relevant data, and improve their overall productivity.


## How to generate your own OpenAI API key

Please watch this video:

[How to Get Your OpenAI API Key](https://www.youtube.com/watch?v=nafDyRsVnXU&ab_channel=TutorialsHub)

## How to Run the project locally

1. Clone the repository 
```bash
git clone https://github.com/url
```

2. Create a virtual environment 
```bash
conda create -n venv python==3.10 -y
```

3. Install the requirements
```bash
pip install -r requirements.txt
```

4. create .env file and paste the API key
```bash
OPENAI_API_KEY=YourAPIKey
```

5. Start the Streamlit server
```bash
streamlit run app.py
```

Enjoy the project.

## Contributions
Contributions to this project are welcome! To contribute, please follow the standard GitHub workflow for pull requests.

## Contact information
If you have any questions or comments about this project, feel free to contact the project maintainer at [Gmail](prajwalgbdr03@gmail.com)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
