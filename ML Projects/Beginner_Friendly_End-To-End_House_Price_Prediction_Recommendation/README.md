
# My Sweet Home - House Price Prediction & Recommendation Project

- [LinkedIn - Rajarshi Roy](https://www.linkedin.com/in/rajarshi-roy-learner/)
  
- [Github - Rajarshi Roy](https://github.com/Rajarshi12321/)

- [Medium - Rajarshi Roy](https://medium.com/@rajarshiroy.machinelearning)
  
- [Kaggle - Rajarshi Roy](https://www.kaggle.com/rajarshiroy0123/)
- [Mail - Rajarshi Roy](mailto:royrajarshi0123@gmail.com)
- [Personal-Website - Rajarshi Roy](https://rajarshi12321.github.io/rajarshi_portfolio/)

## About The Project


Welcome to the My Sweet Home repository, which is a House Price Prediction and Property Recommendation Flask app repository! This app is designed to predict house prices and recommend similar housing properties based on a saved dataset (using content-based filtering). Whether you are a homebuyer looking for your dream house or a real estate investor seeking lucrative opportunities, this app can help you make informed decisions.

## About the Data

The goal is to predict the price of a given Housing Property (Regression Analysis) and also to recommend 6 similar Housing Properties (Content-Based Filtering).

There are 70 independent variables in the raw data, I am here explaining only the important features ( 7 features ) used for feature engineering and model prediction. (To make the task easier I have joined bedroom and bathroom feature as BHK for model prediction and recommendation, Although You can modify it as you like):

 - propertyType: The type or category of the house or property (e.g., apartment, villa, commercial).

 - locality: The specific locality or neighborhood where the house or property is located.

 - furnishing: The level of furnishing provided in the house or property (e.g., fully furnished, semi-furnished, unfurnished).

 - city: Location of the property, setting the context for its surroundings and amenities.
 
 - bedrooms: Number of sleeping spaces available in the property for residents.
 
 - bathrooms:  Count of bathing facilities in the property, indicating convenience and functionality.
 
 - RentOrSale: Specifies whether the property is available for rent or sale, defining its market status.


### Target variable: 
- exactPrice : The exact price of the house or property.
  

Dataset Source Link : [https://www.kaggle.com/datasets/rajarshiroy0123/house-prices-in-india-2023](https://www.kaggle.com/datasets/rajarshiroy0123/house-prices-in-india-2023)

To understand about the feature engineering and model prediction for this particular dataset please refer to the following: </br>
Kaggle Notebook : [https://www.kaggle.com/code/rajarshiroy0123/indian-house-price-prediction](https://www.kaggle.com/code/rajarshiroy0123/indian-house-price-prediction)


## Table of Contents

- [My Sweet Home - House Price Prediction \& Recommendation Project](#my-sweet-home---house-price-prediction--recommendation-project)
  - [About The Project](#about-the-project)
  - [About the Data](#about-the-data)
    - [Target variable:](#target-variable)
  - [Table of Contents](#table-of-contents)
  - [Images](#images)
  - [Installation and Dependencies](#installation-and-dependencies)
  - [Working Directory](#working-directory)
  - [Working with the code](#working-with-the-code)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Contact](#contact)
  - [License](#license)
  - [Reference](#reference)

## Images 

Inputing Features :
![image](https://github.com/Rajarshi12321/Housing_predict_recommend/assets/94736350/2a1f9fff-bf1e-4533-9090-58db6502445d)

Predicted and recommended Output :
![image](https://github.com/Rajarshi12321/Housing_predict_recommend/assets/94736350/60bed2a5-52cc-4c9f-acad-421acf0db3b2)



## Installation and Dependencies

These are some required packages for our program which are mentioned in the Requirements.txt file

- pandas
- numpy
- seaborn
- matplotlib
- scikit-learn
- catboost
- xgboost
- Flask
- dill
- requests
- beautifulsoup4
- bs4
- jinja2
- joblib
- librosa
- lxml




## Working Directory

```
📦Housing_predict_recommend
 ┣ 📂artifact
 ┃ ┗ 📜Dataset.csv
 ┣ 📂artifacts
 ┃ ┣ 📜data_preprocessed_recommend.csv
 ┃ ┣ 📜model.pkl
 ┃ ┣ 📜model_rent.pkl
 ┃ ┣ 📜preprocessor.pkl
 ┃ ┣ 📜processed_data.csv
 ┃ ┣ 📜recommend_data.csv
 ┃ ┗ 📜testing.py
 ┣ 📂catboost_info
 ┣ 📂logs
 ┣ 📂NOTEBOOK
 ┃ ┣ 📂DATA
 ┃ ┃ ┗ 📜Scraped_Data.csv
 ┃ ┗ 📜indian-house-price-prediction.ipynb
 ┣ 📂src
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📜data_ingestion.py
 ┃ ┃ ┣ 📜data_transformation.py
 ┃ ┃ ┣ 📜model_trainer.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂pipeline
 ┃ ┃ ┣ 📜predict_pipeline.py
 ┃ ┃ ┣ 📜scraping_pipeline.py
 ┃ ┃ ┣ 📜train_pipeline.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂recommender
 ┃ ┃ ┣ 📜data_transformation_recommend.py
 ┃ ┃ ┣ 📜house_recommender.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜exception.py
 ┃ ┣ 📜logger.py
 ┃ ┣ 📜utils.py
 ┃ ┗ 📜__init__.py
 ┣ 📂static
 ┃ ┣ 📂css
 ┃ ┃ ┗ 📜signup.css
 ┃ ┗ 📂img
 ┃ ┃ ┣ 📜beautiful_house.jpg
 ┃ ┃ ┣ 📜default_pic.png
 ┃ ┃ ┗ 📜No Suitable house image found.png
 ┣ 📂templates
 ┃ ┣ 📜get_elements.py
 ┃ ┣ 📜home.html
 ┃ ┣ 📜index.html
 ┃ ┗ 📜testing.html
 ┣ 📜.gitignore
 ┣ 📜.gitattributes
 ┣ 📜app.py
 ┣ 📜city_locality.npy
 ┣ 📜Dockerfile
 ┣ 📜LICENSE
 ┣ 📜main.py
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜setup.py
 ```


## Working with the code


I have commented most of the neccesary information in the respective files.

To run this project locally, please follow these steps:-

1. Clone the repository:

   ```shell
   git clone https://github.com/Rajarshi12321/My-Sweet-Home.git
   ```


2. **Create a Virtual Environment** (Optional but recommended)
  It's a good practice to create a virtual environment to manage project dependencies. Run the following command:
     ```shell
     conda create -p <Environment_Name> python==<python version> -y
     ```

3. **Activate the Virtual Environment** (Optional)
   Activate the virtual environment based on your operating system:
      ```shell
      conda activate <Environment_Name>/
      ```

4. **Install Dependencies**
   - Navigate to the project directory:
     ```
     cd [project_directory]
     ```
   - Run the following command to install project dependencies:
     ```
     pip install -r requirements.txt
     ```

   Ensure you have Python installed on your system (Python 3.9 or higher is recommended).<br />
   Once the dependencies are installed, you're ready to use the project.



5. Run the Flask app: Execute the following code in your terminal.
   ```shell  
   python app.py 
   ```
   

6. Access the app: Open your web browser and navigate to http://127.0.0.1:5000/ to use the House Price Prediction and Property Recommendation app.

(Additional Functionality)

1. You can use your own data and form the datasets as per your liking using the pipelines, Change the source of the dataset in data ingestion pipeline in the file directory `src/components/data_ingestion.py`
2. Run the following codes to make your clean, proprocess and make model based on your date (Modify the pre processing pipleline and model making pipeline based on your required result for your project)
   ```shell
   python src/components/data_ingestion.py
   python src/components/data_transformation.py
   python src/components/model_trainer.py
   ``` 
3. Modify the index.html, home.html and app.py to suit your required features.</br>
   These file directories are:</br>
   `app.py` </br>
   `templates/home.html`</br>
   `templates/index.html`

## Usage
1. **House Price Prediction:** On the app's homepage, users can input the specific features of the house they are interested in. After submitting the details, the app will process the information and display the predicted price for the house.

2. **Property Recommendation:** Along with the house price predictions users will also get similar recommendation. The app will provide a list of 6 most similar properties that match the given criteria.

## Contributing
I welcome contributions to improve the functionality and performance of the app. If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.

2. Make your changes and ensure that the code is well-documented.

3. Test your changes thoroughly to maintain app reliability.

4. Create a pull request, detailing the purpose and changes made in your contribution.

## Contact

Rajarshi Roy - [royrajarshi0123@gmail.com](mailto:royrajarshi0123@gmail.com)



## License
This project is licensed under the MIT License. Feel free to modify and distribute it as per the terms of the license.

I hope this README provides you with the necessary information to get started with the Housing Price Prediction and Recommending project. 

## Reference

I took reference from Krish Naik sir's [YouTube Playlist](https://youtube.com/playlist?list=PLZoTAELRMXVPS-dOaVbAux22vzqdgoGhG&si=WpPn00reSU9yYZzc).

