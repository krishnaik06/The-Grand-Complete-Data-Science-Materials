# Retrieval Augmented Generation (RAG) Application using LLMs

## Overview
Welcome to the Retrieval Augmented Generation (RAG) project! This repository contains the implementation of advanced retrieval methods to enhance the integration of large language models (LLMs) with proprietary data. The primary goal is to improve the coherence and performance of the RAG pipeline through two advanced retrieval methods: Sentence-window retrieval and Auto-merging retrieval.

## Files
**Medical_Cost_Prediction.pdf**: This is the pdf used to query information, it contains details about one of my previous projects - Medical Cost Prediction using Machine Learning for AWS Deployment.

**RAG_Pipeline.ipynb**: Jupyter notebook that encompasses the implementation of the basic RAG pipeline, which serves as the baseline for comparing and evaluating the advanced RAG techniques.

**automerging_retrieval.ipynb**: Jupyter Notebook focusing on the implementation and details of the auto-merging retrieval method. This file provides insights into how this method enhances the baseline RAG pipeline.

**sentence_window_retrieval.ipynb**: Jupyter notebook dedicated to the implementation and details of the sentence-window retrieval method. It elaborates on how this retrieval method contributes to improving the RAG pipeline.

**utils.py**: A Python script containing utility functions and helper methods used across notebooks. This file is crucial for the modular and organized implementation of the project.

**default.sqlite**: A SQLite database file, possibly storing relevant data or configurations needed for the project. Please refer to the specific notebooks to understand their usage.

**questions.txt**: A text file containing evaluation questions. These questions are used for assessing the performance of the RAG pipeline, based on the RAG triad: Context Relevance, Groundedness, and Answer Relevance.

## Evaluating and Experiment Tracking
To evaluate and iteratively improve the RAG pipeline's performance, follow these steps:

Run each notebook in the project structure and focus on TruLens Evaluation and the parameters used.

Sentence-Window Retrieval - Concentrate on the window size, which indicates the number of sentences preceding and following a particular sentence that should be taken into account to provide sufficient context.

Auto-Merging Retrieval - Focus on the depth of the tree; the greater the number of layers, the fewer tokens in the leaf nodes (only nodes are used in constructing a VectorStore Index), resulting in lower costs for the Language Model (LLM).

## Contribution Guidelines
If you wish to contribute to the project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes and ensure the code is well-documented.
4. Submit a pull request, explaining the changes and improvements.

Thank you for contributing to the Retrieval Augmented Generation (RAG) project!

## Authors   
- Anirudh Nuti - *Initial Work* - [NVK Anirudh](https://github.com/NvkAnirudh)

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/NvkAnirudh/RAG_Application_Using_LLMs/blob/main/LICENSE) file for details

## Acknowledgements
This project serves as a practical exercise from the [course](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/)


