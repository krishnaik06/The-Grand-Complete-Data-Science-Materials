# Heart Disease Prediction

- LinkedIn [Hema Kalyan Murapaka](https://www.linkedin.com/in/hemakalyan)
- Medium [KalyanMurapaka274](https://medium.com/@kalyanmurapaka274)


## About The Project


Heart disease prediction is a crucial aspect of preventive healthcare that involves the comprehensive analysis of diverse data points to evaluate an individual's susceptibility to cardiovascular diseases. This process integrates demographic details like age and gender with critical clinical information, including medical and family histories, lifestyle choices, and existing health conditions such as hypertension or diabetes. By examining biomarkers like blood pressure, cholesterol levels, and blood sugar, alongside results from medical tests and imaging studies, predictive models can identify patterns and trends indicative of potential heart issues. Machine learning algorithms play a pivotal role in processing this information, helping stratify individuals into risk categories. The ultimate goal is to enable timely interventions and personalized preventive strategies, empowering individuals to make lifestyle adjustments that can mitigate the risk of heart-related events like heart attacks or strokes. Continuous monitoring and updating of predictive models ensure ongoing accuracy and effectiveness in supporting proactive heart health management.

## About the Dataset

This dataset gives information related to heart disease. The dataset contains 13 columns, target is the class variable which is affected by the other 12 columns. Here the aim is to classify the target variable to (disease\non disease) using different machine learning algorithms and find out which algorithm is suitable for this dataset.
<br><be>

<h3>Attributes:</h3> 

 - Age 
 - Gender 
 - Chest Pain Type
 - Resting Blood Pressure
 - Serum Cholesterol 
 - Fasting Blood Sugar 
 - Resting Electrocardiographic Results
 - Maximum Heart Rate Achieved
 - Exercise-induced angina
 - Depression induced by exercise relative to rest
 - Slope of the Peak Exercise ST Segment
 - Number of Major Vessels Colored by Fluoroscopy
 - Thalassemia
 - Target 

## Built With

 - Pandas
 - Numpy
 - Scikit-Learn
 - Seaborn
 - Matplotlib
 - Flask
 - DVC (Data Version Control)
 - MLFlow
 - Catboost
 - XG Boost

## Getting Started

This will help you understand how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

## Installation Steps

### Option 1: Installation from GitHub

Follow these steps to install and set up the project directly from the GitHub repository:

1. **Clone the Repository**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to install the project.
   - Run the following command to clone the GitHub repository:
     ```
     git clone https://github.com/KalyanMurapaka45/Heart-Disease-Prediction.git
     ```

2. **Create a Virtual Environment** (Optional but recommended)
   - It's a good practice to create a virtual environment to manage project dependencies. Run the following command:
     ```
     conda create -p <Environment_Name> python==<python version> -y
     ```

3. **Activate the Virtual Environment** (Optional)
   - Activate the virtual environment based on your operating system:
       ```
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

5. **Run the Project**
   - Start the project by running the appropriate command.
     ```
     python app.py
     ```

6. **Access the Project**
   - Open a web browser or the appropriate client to access the project.
  
<br><br>
### Option 2: Installation from DockerHub

If you prefer to use Docker, you can install and run the project using a Docker container from DockerHub:

1. **Pull the Docker Image**
   - Open your terminal or command prompt.
   - Run the following command to pull the Docker image from DockerHub:
     ```
     docker pull kalyan45/heart-app
     ```

2. **Run the Docker Container**
   - Start the Docker container by running the following command, and mapping any necessary ports:
     ```
     docker run -p 5000:5000 kalyan45/heart-app
     ```

3. **Access the Project**
   - Open a web browser or the appropriate client to access the project.

## Setup

### MLflow Tracking

We use MLflow to log and track our machine learning experiments. The MLFLOW_TRACKING_URI environment variable is set to the DagsHub repository's MLflow tracking URI.

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/HemaKalyan45/Heart-Disease-Prediction.mlflow

export MLFLOW_TRACKING_USERNAME=HemaKalyan45

export MLFLOW_TRACKING_PASSWORD=f3c9457eb0ff83244e93ac8ee651b80d4b35f07c
```

## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


## Contact

Hema Kalyan Murapaka - [@kalyanmurapaka274@gmail.com](kalyanmurapaka274@gmail.com)


## Acknowledgements

We'd like to extend our gratitude to all individuals and organizations who have played a role in the development and success of this project. Your support, whether through contributions, inspiration, or encouragement, has been invaluable. Thank you for being a part of our journey.
