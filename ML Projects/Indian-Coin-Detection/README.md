# Indian-Coin-Detection


# Linkedin
linkedin.com/in/pradhan-debasish
# Email
pradhandebasish2046@gmail.com





# Dataset 
https://www.kaggle.com/datasets/pradhandebasish/indian-coin-detection



https://github.com/pradhandebasish2046/Indian-Coin-Detection/assets/84903046/e0a4a1a0-1f85-49f8-bdc7-7d001a5ba25b




## Workflows


1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py
9. Update the dvc.yaml


## Project Archietecture
![Project Archietecture](https://github.com/pradhandebasish2046/Indian-Coin-Detection/assets/84903046/569a365d-d1cb-4739-bf22-d7e2945e6c77)


## Deployment Archietecture
![Deployment Archietecture](https://github.com/pradhandebasish2046/Indian-Coin-Detection/assets/84903046/1437f42d-37a7-48d5-866f-f86f77214348)



## File Structure
![File structure](https://github.com/pradhandebasish2046/Indian-Coin-Detection/assets/84903046/53d2c74c-3ee5-4644-9819-8ec101da13e3)



# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/pradhandebasish2046/Indian-Coin-Detection.git
```
### STEP 01- Create a python environment after opening the repository. Then activate the environment


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
streamlit run app.py
```

Now,
```bash
open up you local host and port
```


### DVC cmd

1. dvc init
2. dvc repro
3. dvc dag




# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the URI: 566373416292.dkr.ecr.us-east-1.amazonaws.com/indian-coin-detection

	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

    AWS_ACCESS_KEY_ID

    AWS_SECRET_ACCESS_KEY

    AWS_REGION = ap-south-1

    AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

    ECR_REPOSITORY_NAME = simple-app
