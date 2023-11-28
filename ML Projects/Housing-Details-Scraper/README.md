

# Housing Information Scrapping


- [LinkedIn - Rajarshi Roy](https://www.linkedin.com/in/rajarshi-roy-learner/)
  
- [Github - Rajarshi Roy](https://github.com/Rajarshi12321/)

- [Medium - Rajarshi Roy](https://medium.com/@rajarshiroy.machinelearning)
  
- [Kaggle - Rajarshi Roy](https://www.kaggle.com/rajarshiroy0123/)
- [Mail - Rajarshi Roy](mailto:royrajarshi0123@gmail.com)
- [Personal-Website - Rajarshi Roy](https://rajarshi12321.github.io/rajarshi_portfolio/)

## About The Project

Welcome to the Housing Information Scrapping repository! This project focuses on scraping features of houses from Magicbricks.com using SCRAPY and SELENIUM. The goal is to scrape this data and generate a dataset to analyze the housing prices and also make House price predicting models based on real and recent scraped data.

## Built With

 - Selenium
 - Scrapy

## Table of Contents

- [Housing Information Scrapping](#housing-information-scrapping)
  - [About The Project](#about-the-project)
  - [Built With](#built-with)
  - [Table of Contents](#table-of-contents)
  - [Installation and Dependencies](#installation-and-dependencies)
  - [Working with the code](#working-with-the-code)
  - [Results](#results)
  - [Contributing](#contributing)
  - [Contact](#contact)
  - [License](#license)



## Installation and Dependencies

These are some required packages for our program which are mentioned in the Requirements.txt file

- scrapy   
- pathlib
- scrapy-fake-useragent 
- pandas 
- selenium 


To run this project locally, please follow these steps:

1. **Clone the Repository**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to install the project.
   - Run the following command to clone the GitHub repository:
   
      ```shell
      git clone https://github.com/Rajarshi12321/House_prices_scraped.git

2. **Create a Virtual Environment** (Optional but recommended)
   - It's a good practice to create a virtual environment to manage project dependencies. Run the following command:
  
      ```shell
      conda create -p <Environment_Name> python==<python version> -y
      ```
3. **Activate the Virtual Environment** (Optional)
   - Activate the virtual environment based on your operating system:
       ```
       conda activate <Environment_Name>/
       ```
4. **Install Dependencies**
   - Navigate to the project directory:
     ```shell
     cd [project directory]
     ```

     In this case:
     ```shell
     cd Housing-Details-Scraper
     ```
   - Run the following command to install project dependencies:
     ```shell
     pip install -r requirements.txt
     ```


## Working with the code
Before starting out with the program, I had checked the html of the website and how the json files were stored in the script tags. It was a good experience for me to collect data from these scripts and use xpaths.

(Optional) You can checkout the website html for better understanding of the program

I have commented most of the neccesary information in the House_princing.py in spiders folder.

Now to run the program :-

1. Activating the env
  
   ```shell
   conda activate <Environment_Name>/
   ```

2. Going the main file by changing directory
   ```shell
   cd House_price
   ```

3. Running the file to scrape the data
   
   ```shell
   scrapy crawl House_pricing -o <filename>
   ```
   For Example
   ```shell
   scrapy crawl House_pricing -o items.csv
   ```
  This filename is where your scraped data would be stored,the data can be stored in .csv , .json or other type of files according to what type you will choose


## Results
The results of the project : This project is able to scrape 27900 data with 70+ features

You can check out the scrapped data that I published on [kaggle](https://www.kaggle.com/datasets/rajarshiroy0123/house-prices-in-india-2023)


## Contributing
Contributions to this project are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request. Let's work together to enhance the scrape data and make the program more accurate.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request


## Contact

Rajarshi Roy - [royrajarshi0123@gmail.com](mailto:royrajarshi0123@gmail.com)

## License
This project is licensed under the MIT License. Feel free to modify and distribute it as per the terms of the license.

We hope this README provides you with the necessary information to get started with the Housing Information Scrapping project. Happy scraping data!
