
# Importing basic modules
import requests
import time

# Initialization
HOST_URL = "localhost"
API_VERSION = "v1.0"
PREDICTION_PORT = 8001
transcript_location = "../../../sample_data/sample_transcript.txt"
summary_location = "../../../sample_data/sample_summary.txt"

# reading transcript from the file
with open(transcript_location) as sample_file:
    transcript_data = sample_file.read()

# reading summary from the file
with open(summary_location) as sample_file:
    summary_data = sample_file.read()

def client_script():
 
    # Prediction Module
    try:
        st = time.time()
        result = requests.post(f'http://{HOST_URL}:{PREDICTION_PORT}/{API_VERSION}/prediction',
                                headers={'Content-type': 'application/json'},
                                json={'title': 'test title', 'model': 'all-mpnet-base-v2',
                                        'transcript': transcript_data, 'summary' : summary_data
                                        }
                                )
        et = time.time()
        if result.status_code == 201 or result.status_code == 200:
            print(result.json())
            print(f'Inference Time : {et-st}')
        elif result.status_code == 422:
            print('INVALID INPUT - TITLE, SUMMARY(MIN 30 CHARACTERS), TRANSCRIPT(MIN 30 CHARACTERS) AND MODEL NAME SHOULD BE IN STRING FORMAT')
        elif result.status_code == 500:
            print('MODULE EXECUTION ERROR')
        elif result.status_code == 404:
            print('INVALID MODEL NAME')
    except:
        print('CLIENT MODULE EXECUTION ERROR')


client_script()