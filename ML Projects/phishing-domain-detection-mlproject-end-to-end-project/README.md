![Phishing classifier - Google Chrome 2022-08-22 12-20-50](https://user-images.githubusercontent.com/52929512/185863089-ad6a21b7-68d1-43cc-832f-d65140e7b388.gif)
# Phishing_domain_detection_mlproject

An AI solution to detect whether the domain is real or malicious

This application takes inputs related to a URL's features and depending upon that, it predicts whether the website is malicious or not.

This ML application is based on XGBoost model as it gave 95% accuracy(maximum among all the given algorithm)

## Dataset

The dataset available for this application is present on https://data.mendeley.com/datasets/72ptz43s9v/1

It has 2 files one as a small variant and other for the large variant.ML Model present in this repository is trained on the larger variant.

## Installation
Create virtual environment for python 3.7

```bash
  conda create -n <environment-name> python=3.7 -y
```
Enter the virtual environment
```bash
    activate <environment-name>
```
install all dependencies of the this project by 
```bash
  pip install -r requirements.txt
```
    
## Notebooks

To understand preprocessing steps please click link [EDA and preprocessing notebook](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/notebooks/EDA%20and%20preprocessing.ipynb)


To understand model selection and Hyperparameter tuning steps please click [optuna jupyter Notebook](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/notebooks/optuna.ipynb)

## Documents
For HLD document please click link [HLD Document](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/docs/Phishing_Domain_Detector_HLD_1.1.pdf)

For LLD document please click link [LLD Document](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/docs/Phishing_Domain_Detector_LLD_1.0.pdf)

For wireframe design document please click link [wireframe Design Document](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/docs/Wireframe%20Design.pdf)

For System architecture document please click link [System architecture Document](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/docs/Architecture_document.pdf)

For DPR(detailed project report) document please click link [DPR](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/docs/Phishing-domain-detection.pdf)


## Deployment

I used CI-CD pipeline to deploy this application to heroku and the pipeline was created through Github actions.

You have provide your heroku credentials like email-id,heroku_api_key,heroku app name in github actions secrets section

To deploy this project first write the Dockerfile having this commands

```bash
FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=3 --bind 0.0.0.0:$PORT src.main:app
```

Then go to .github/workflows/main.yaml and write this code to enable CI-CD pipeline on the master branch
```bash
# Your workflow name.
name: Deploy to heroku.

# Run workflow on every push to main branch.
on:
  push:
    branches: [master]

# Your workflows jobs.
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Check-out your repository.
      - name: Checkout
        uses: actions/checkout@v2
      - name: Build, Push and Release a Docker container to Heroku. # Your custom step name
        uses: gonuit/heroku-docker-deploy@v1.3.3 # GitHub action name (leave it as it is).
        with:
          # Below you must provide variables for your Heroku app.

          # The email address associated with your Heroku account.
          # If you don't want to use repository secrets (which is recommended) you can do:
          # email: my.email@example.com
          email: ${{ secrets.HEROKU_EMAIL }}

          # Heroku API key associated with provided user's email.
          # Api Key is available under your Heroku account settings.
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}

          # Name of the heroku application to which the build is to be sent.
          heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}

          # (Optional, default: "./")
          # Dockerfile directory.
          # For example, if you have a Dockerfile in the root of your project, leave it as follows:
          dockerfile_directory: ./

          # (Optional, default: "Dockerfile")
          # Dockerfile name.
          dockerfile_name: Dockerfile

          # (Optional, default: "")
          # Additional options of docker build command.
          docker_options: "--no-cache"

          # (Optional, default: "web")
          # Select the process type for which you want the docker container to be uploaded.
          # By default, this argument is set to "web".
          # For more information look at https://devcenter.heroku.com/articles/process-model
          process_type: web
```



## Hosted Heroku API
https://phishing-domain-detector123.herokuapp.com/


## Performance Metrics
![Alt text](https://github.com/saurabhznaikz/phishing_domain_detection_mlproject/blob/master/docs/performance_matrix.png?raw=true "Optional Title")

