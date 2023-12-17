# Getting Started with Multimodal model - Gemini Pro and Gemini Pro Vision

This tutorial is intended for getting hands on quickly with Gemini Pro and Gemini Pro Vision.

- We will be using Google AI Studio library for Text to Text Examples and Image Question and Answering tasks.
- For Video Question and Answering, we will be using Vertex AI library.

## Prerequisites

- Have Anaconda install and is initialized to the terminal.

### Getting Google AI Studio API Key

- Go to [Google AI for Developers](https://ai.google.dev) and click on "Get API key Google AI Studio".
- Click on Get API Key followed by clicking Create API Key in new project or Create API Key in existing project.

### Creating Google Service Account

- We will be requiring this account for Video Question and Answering.
- Create Google Cloud Service Account - with the role of Vertex AI Adminstrator.
- Once the service account is created, click on that service account, followed by click on Keys, Add Key, select JSON and click on Create which will then allow to download json file that includes service account credentials.

### `.env` file

`.env` file should have following content. It should be in the same folder as this README.md file.

```bash
GOOGLE_AI_STUDIO="API_KEY_OBTAINED_FROM_GOOGLE_AI_STUDIO"
GOOGLE_APPLICATION_CREDENTIALS=relative_location_path_of_json_file_that_includes_service_account_details
GEMINI_PRO="gemini-pro"
GEMINI_PRO_VISION="gemini-pro-vision"
```

## Creating Conda Environment

1. Create new conda environment.

```bash
conda create -n google_gemini_environment python=3.11
```

2. Install the requirements

```bash
pip install -r requirements.txt
```

3. Activate the environment

```bash
conda activate google_gemini_environment
```

Now, we are ready to dive into the tutorials.

## Tutorials

All are documented in the Notebooks in the research folder.

## References

- Sam Witeeven: https://www.youtube.com/watch?v=HN96QDFBD0g&t=24s&ab_channel=SamWitteveen
- Google Generative AI Tutorials: https://cloud.google.com/vertex-ai/docs/generative-ai/tutorials
