# diabeteasy
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

Diabeteasy, an application that detects diabetes, connects users to nearby top-rated doctors, and
simplifies medicine tracking.



# Getting Started
### Prerequisites
To run Diabeteasy on your local device, you will need to have the following installed:

- Python 3
- Pip

### Installation
Install the required packages
```
pip install -r requirements.txt

```
Get the API key from GMAP API and put it in app.secret_key.
```app.secret_key = 'YOUR GMAP API KEY'```

start the app

```
pyhton app.py

```

### Landing page
![landing-page](https://user-images.githubusercontent.com/70543525/226149291-0c92038a-051a-450e-b9c5-4782e24ebd60.png)

### Sign up page (user must signup and then login before using di-detector)
![signup](https://user-images.githubusercontent.com/70543525/226149294-31c5d032-ceb8-4d2c-b11d-6ba51e33756d.png)

### Login Page
![login](https://user-images.githubusercontent.com/70543525/226149297-7256fa89-5408-4ac5-839f-efb2f4d567a2.png)

### Form that accepts input from user to predict their diabetes
![di-detector](https://user-images.githubusercontent.com/70543525/226149314-1c3a6889-a6c3-4da9-8aba-428b12285cca.png)
### Message after the algo detects the diabetes 
![detected](https://user-images.githubusercontent.com/70543525/226149328-31080a9b-acf2-4a6e-9d6b-9e0654c591bf.png)
### Doctor recommendations based on input location and medication trcaking system 
#### You have to wait for 10-15 sec to load outputs of GMap API response
![suggestions](https://user-images.githubusercontent.com/70543525/226149353-face69a4-a36a-49f3-9e7f-fa37905bcb1a.png)

