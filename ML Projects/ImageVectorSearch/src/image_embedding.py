from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
import cv2
import os
import random
import csv
from glob import glob
from pathlib import Path
from statistics import mean
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility, MilvusClient
from datetime import datetime
# from config import *
import requests
from PIL import Image
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
import os
import io
import swifter
import sys

# Load environment variables from the .env file
load_dotenv("../.env")


class ImageEmbed:
    def __init__(self):
        """
        Initialize the ImageEmbed class.

        Attributes:
        - model: ResNet50 model for image embedding
        - HOST: Milvus host (IP address or domain)
        - PORT: Milvus port number
        - DIM: Dimension of embedding extracted by the model
        - COLLECTION_NAME: Name of the Milvus collection for reverse image search
        - INDEX_TYPE: Type of Milvus index used for searching
        - METRIC_TYPE: Type of Milvus metric used for measuring similarity
        - batch_size: Batch size for processing and inserting images into Milvus
        - failure_data: List to store data for failed operations
        - image_csv: Path to the CSV file containing image data
        - style_csv: Path to the CSV file containing style data
        """
        # Initialize ResNet50 model for image embedding
        self.model = ResNet50(include_top=False, weights='imagenet', pooling='avg')

        # Milvus configuration
        self.HOST = os.getenv("HOST")  # Milvus host (IP address or domain)
        self.PORT = os.getenv("PORT")  # Milvus port number
        self.DIM = int(os.getenv("DIM"))  # Dimension of embedding extracted by the model
        self.COLLECTION_NAME = os.getenv("COLLECTION_NAME")  # Name of the Milvus collection for reverse image search
        self.INDEX_TYPE = os.getenv("INDEX_TYPE")  # Type of Milvus index used for searching
        self.METRIC_TYPE = os.getenv("METRIC_TYPE")  # Type of Milvus metric used for measuring similarity
        self.batch_size = int(os.getenv("BATCH_SIZE"))  # Batch size for processing and inserting images into Milvus

        # Data and file paths
        self.failure_data = list()  # List to store data for failed operations
        self.image_csv = "../data/images.csv"  # Path to the CSV file containing image data
        self.style_csv = "../data/styles.csv"  # Path to the CSV file containing style data

    def image_embedding(self, img_url: str) -> list[float]:
        """
        Calculate the CNN image embedding for an image from a URL.

        :param img_url: URL of an image in jpeg, jpeg, png, webp format
        :return: CNN Image Embedding as a list of floats
        """
        try:
            # Download the image from the URL
            response = requests.get(img_url)
            response.raise_for_status()  # Check for any request errors
            image_data = response.content

            # Convert image data to an image object
            img = Image.open(io.BytesIO(image_data))

            # Process the image and calculate the embedding
            img = img.convert("RGB")  # Ensure the image is in RGB format
            img = img.resize((224, 224))  # Resize the image to the target size

            # Convert image to array, expand dimensions, and preprocess for the model
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Calculate the image embedding using the pre-trained model
            embedding = self.model.predict(x)

            # Return the embedding as a list of floats
            return list(embedding[0])

        except requests.exceptions.RequestException as e:
            # Handle the case when there is an issue with downloading the image
            print(f"Failed to download image from URL: {img_url}. Error: {e}")
            return None

        except Exception as e:
            # Handle other unexpected errors
            print(f"Some issue has occurred: {e}")
            return None

    def data_loader(self) -> pd.DataFrame:
        """
        Load data from the CSV files and prepare it for processing.

        :return: DataFrame with '_id' and 'images' fields
        """
        try:
            # Load image data from CSV
            images = pd.read_csv(self.image_csv)
            # Extract 'id' from the 'filename' column and convert it to int64
            images["id"] = images["filename"].str.replace(".jpg", "").astype("int64")
            # Limit the number of rows to 15
            images = images.head(15)
            # Load style data from CSV
            styles = pd.read_csv(self.style_csv)
            # Merge image and style data on 'id'
            data = pd.merge(images, styles, how="left", on="id")
            # Select only the necessary columns
            data = data[['id', 'link']]
            # Convert 'id' to int for consistency
            data["id"] = data["id"].astype(int)
            # Return the prepared DataFrame
            return data
        except FileNotFoundError as e:
            # Handle the case when one or both CSV files are not found
            print(f"Error loading data: {e}")
            return pd.DataFrame()
        except Exception as e:
            # Handle other unexpected errors
            print(f"Some issue has occurred: {e}")
            return pd.DataFrame()

    def create_milvus_collection(self):
        """
        Create a Milvus collection and define the schema.

        :return: Milvus Collection object
        """
        try:
            # Check if the collection already exists
            if utility.has_collection(self.COLLECTION_NAME):
                collection = Collection(self.COLLECTION_NAME)
                return collection

            # Define the field schema for the collection
            fields = [
                FieldSchema(name='id', dtype=DataType.INT64, description='id', max_length=500, is_primary=True, auto_id=False),
                FieldSchema(name='link', dtype=DataType.VARCHAR, description='image urls', max_length=500),
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='Image embedding vectors', dim=self.DIM)
            ]

            # Define the collection schema
            schema = CollectionSchema(fields=fields, description='Reverse image search')

            # Create the Milvus collection
            collection = Collection(name=self.COLLECTION_NAME, schema=schema, enable_dynamic_field=True)

            # Create the indexing for the 'embedding' field
            index_params = {
                'metric_type': self.METRIC_TYPE,
                'index_type': self.INDEX_TYPE,
                'params': {"nlist": self.DIM}
            }
            collection.create_index(field_name='embedding', index_params=index_params)

            print(f'A new collection created: {self.COLLECTION_NAME}')
            return collection

        except Exception as e:
            # Handle unexpected errors
            print(f"Error creating Milvus collection: {e}")
            return None

    def load_data(self):
        """
        Load and process data, insert it into the Milvus collection.

        :return: Milvus Collection object
        """
        try:
            # Connect to Milvus server
            connections.connect(host=self.HOST, port=self.PORT)

            # Create or get the Milvus collection
            collection = self.create_milvus_collection()

            # Get the number of entities in the collection
            num_entities = collection.num_entities
            print("Number of entities:", num_entities)

            # Load and process data from CSV files
            data = self.data_loader()

            # Insert processed data into the Milvus collection
            self.insert_bulk_data(collection=collection, data=data)

            # Load the Milvus collection
            collection.load()

            # Select a random row from the data
            random_row = data.sample(n=1)

            # Get the 'link' column value from the selected row
            selected_link = random_row['link'].values[0]

            # Search for the image in the Milvus collection using the selected link
            self.search_image(collection=collection, url=selected_link)

            print("Processes Completed..", datetime.now() - start)

            # Save failure data to a CSV file if any
            if self.failure_data:
                file_name = f"FAILURE_URL_{datetime.now()}"
                pd.DataFrame(self.failure_data).to_csv(file_name)
                print(f"Failure data file {file_name}")

            # Return the Milvus collection
            return collection

        except Exception as e:
            # Handle unexpected errors
            print(f"Error loading data: {e}")
            return None

    def insert_bulk_data(self, collection, data):
        """
        Insert processed data into the Milvus collection.

        :param collection: Milvus Collection object.
        :param data: DataFrame containing processed data.
        """
        try:
            # Calculate image embeddings for each 'link' in the data
            data["embedding"] = data["link"].swifter.apply(self.image_embedding)

            # Identify and store records with embedding calculation failures
            self.failure_data.extend(data[data["embedding"].isna()].to_dict(orient="records"))

            # Filter out records with successful embeddings
            batch_data = data[data["embedding"].notna()]

            # Insert the batch data into the Milvus collection
            collection.insert(batch_data.to_dict(orient="records"))

        except Exception as e:
            # Handle unexpected errors during data insertion
            print(f"Error inserting bulk data into Milvus collection: {e}")

    def insert_data_batched(self, collection, data):
        """
        Insert data into Milvus collection in batches to avoid memory issues.

        :param collection: Milvus Collection object.
        :param data: DataFrame containing data to be inserted.
        """
        try:
            # Calculate the number of batches based on the batch size
            batch_count = len(data) // self.batch_size
            print("batch_count: ", batch_count)

            # Iterate over batches
            for i in tqdm(range(batch_count + 1), desc="Batch Loop"):
                start = i * self.batch_size
                end = (i + 1) * self.batch_size

                # Extract a batch of data
                batch_data = data[start:end]

                # Calculate embeddings for the 'link' column in the batch
                batch_data["embedding"] = batch_data["link"].swifter.apply(self.image_embedding)

                # Identify and store records with embedding calculation failures
                self.failure_data.extend(batch_data[batch_data["embedding"] is None].to_dict(orient="records"))

                # Filter out records with successful embeddings
                batch_data = batch_data[batch_data["embedding"].notna()]

                # Print columns and shape information for the batch
                print("Columns: ", batch_data.columns, batch_data.shape)

                # Insert the batch data into the Milvus collection
                collection.insert(batch_data.to_dict(orient="records"))

        except Exception as e:
            # Handle unexpected errors during batched data insertion
            print(f"Error inserting batched data into Milvus collection: {e}")

    def search_image(self, collection, url):
        """
        Search for similar images in the Milvus collection based on the provided image URL.

        :param collection: Milvus Collection object.
        :param url: URL of the image for similarity search.
        """
        try:
            print("url: ", url)

            # Calculate the embedding for the provided image URL
            image_embedding = self.image_embedding(url)

            # Set up parameters for the Milvus collection search
            search_param = {
                "data": [image_embedding],
                "anns_field": "embedding",
                "param": {"metric_type": "L2", "offset": 0},
                "limit": 11,
            }

            start = datetime.now()

            # Perform the similarity search in the Milvus collection
            res = collection.search(**search_param)

            # Extract hits from the search result
            hits = res[0]

            # Print query time and predicted images
            print("query time: ", datetime.now() - start)
            print("Predicted images")
            print(hits.ids)
            return hits.ids

        except Exception as e:
            # Handle unexpected errors during image search
            print(f"Error searching for similar images: {e}")
            return []


if __name__ == '__main__':
    image_embed = ImageEmbed()
    image_embed.load_data()
