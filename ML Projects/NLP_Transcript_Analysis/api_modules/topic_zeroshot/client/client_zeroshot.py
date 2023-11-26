# Importing basic modules
import requests
import time

# Initialization
ZERO_URL = "localhost"
API_VERSION = "v1.0"
ZEROSHOT_PORT = 8001
summary_location = "../../../sample_data/sample_summary.txt"


# reading summary from the file
with open(summary_location) as sample_file:
    summary_data = sample_file.read()


def client_script():
    # Prediction Module
    try:
        st = time.time()
        result = requests.post(f'http://{ZERO_URL}:{ZEROSHOT_PORT}/{API_VERSION}/prediction',
                               headers={'Content-type': 'application/json'},
                               json={'title' : 'test title', 'model': 'bart-large-mnli',
                                     'summary': summary_data, 'labels' : ['sports','music']}
                               )

        et = time.time()
        if result.status_code == 201 or result.status_code == 200:
            print(result.json())
            print(f'Inference Time : {et - st}')
        elif result.status_code == 422:
            print('INVALID INPUT - TITLE, SUMMARY(MIN 20 CHARACTERS) AND MODEL NAME SHOULD BE IN STRING FORMAT')
        elif result.status_code == 500:
            print('MODULE EXECUTION ERROR')
        elif result.status_code == 404:
            print('INVALID MODEL NAME')
    except:
        print('ZEROSHOT MODULE CLIENT ERROR')


client_script()