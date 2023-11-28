import requests
import sys
from bs4 import BeautifulSoup
from src.exception import CustomException


class ImageScrappingPipeline:
    def __init__(self):
        pass

    def scrape_div_content(url):
        try:
            # Step 1: Fetch the HTML content of the webpage
            response = requests.get(url)
            response.raise_for_status()  # Check for any errors in the request

            # Step 2: Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'lxml')

            # Step 3: Locate the desired div element
            div_element = soup.find(
                'div', {'class': "mb-ldp__dtls__photo__fig"})

            # Step 4: Extract the content of the div element
            try:
                div_element = soup.find(
                    'div', {'class': "mb-ldp__dtls__photo__fig"})
                img_div = div_element.find("img")
                return img_div.get("src")
            except:
                return "static/img/default_pic.png"
        except requests.exceptions.RequestException as e:
            return "Error fetching the page: {}".format(e)
        except Exception as e:
            raise CustomException(e, sys)

    def get_images(dataframe):
        try:
            dataframe["image"] = dataframe["URLs"].apply(
                ImageScrappingPipeline.scrape_div_content)
            return dataframe

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    import pandas as pd

    Data_path = "artifacts/recommend_data.csv"
    Dataset = pd.read_csv(Data_path)

    img_pipeline = ImageScrappingPipeline
    img_pipeline.get_images(Dataset.head(n=5))
