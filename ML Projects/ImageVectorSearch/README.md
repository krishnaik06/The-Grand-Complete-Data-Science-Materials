# ImageVectorSearch

ImageVectorSearch is an open-source project that provides a reverse image search engine based on image embeddings. It uses ResNet50 for image embedding generation and Milvus for efficient and scalable image similarity searches.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Generate Image Embeddings](#generate-image-embeddings)
  - [Load Data into Milvus](#load-data-into-milvus)
  - [Search for Similar Images](#search-for-similar-images)
- [Configuration](#configuration)
- [Vector Database](#vector-database)
- [Contributors](#contributors)


## Overview

ImageVectorSearch leverages state-of-the-art deep learning models to generate image embeddings and utilizes Milvus, an open-source vector database, for efficient similarity searches. The project aims to provide a simple and scalable solution for reverse image searches.

## Features

- Image embedding generation using ResNet50.
- Milvus integration for storing and searching image embeddings.
- Batch processing for data loading to Milvus.
- FastAPI integration for querying and retrieving similar images.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
   cd <YOUR_REPO_NAME>

2. Install dependencies:
    
   pip install -r requirements.txt

## Usage
### Generate Image Embeddings

    To generate image embeddings for a given URL, use the following code snippet:
    ```bash
    from image_embedding import ImageEmbed
    image_embed = ImageEmbed()
    embedding = image_embed.image_embedding("<IMAGE_URL>")
    print("Image Embedding:", embedding)
   
### Load Data into Milvus

   To load and process data and insert it into Milvus, run the following code:
    ```bash
    from image_embedding import ImageEmbed
    image_embed = ImageEmbed()
    image_embed.load_data()

### Search for Similar Images 

    To search for similar images given a URL, use the following code:
    ```bash
    from image_embedding import ImageEmbed
    image_embed = ImageEmbed()
    image_embed.search_image("<IMAGE_URL>")
   
## Configuration
Ensure you have a .env file in the root directory with the following variables:

    HOST=<MILVUS_HOST>
    PORT=<MILVUS_PORT>
    DIM=<EMBEDDING_DIMENSION>
    COLLECTION_NAME=<MILVUS_COLLECTION_NAME>
    INDEX_TYPE=<MILVUS_INDEX_TYPE>
    METRIC_TYPE=<MILVUS_METRIC_TYPE>
    BATCH_SIZE=<BATCH_SIZE>

Replace <MILVUS_HOST>, <MILVUS_PORT>, and other placeholders with your actual Milvus configuration.

## Vector Database
Install and run Milvus by following the instructions in the 
Milvus Documentation https://milvus.io/docs/install_standalone-docker.md



## Contributors

```python
contributors = {
    'Akash Saxena': {
        'email': '[akash_saxena](akash26121992@gmail.com)',
        'GitHub': '[akash_saxena](https://github.com/skynoid2612)',
        'LinkedIn': '[akash_saxena](https://www.linkedin.com/in/as26/)'
    }
}