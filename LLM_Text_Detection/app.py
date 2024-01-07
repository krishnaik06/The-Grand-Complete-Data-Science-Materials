import os
from flask import Flask, render_template, request
from src.pipeline.model_prediction_pipeline import PredictionPipeline

# First train the model 
'''
Here, I will skip this step as I am using a CPU machine and I will train the model on the Colab notebook outside the local machine.
'''
# try:
#     # run the command
#     os.system("python main.py")
# except Exception as e:
#     print("Training failed, Not done.")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        predictor = PredictionPipeline(text)
        label = predictor.predict_label()  
        if label == 1:
            label = "Large Language Model"
        elif label == 0:
            label = "Human"
        return render_template('index.html', result=label)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000)
