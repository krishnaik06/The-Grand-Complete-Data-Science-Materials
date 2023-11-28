from flask import Flask, request, render_template
from src.Heart.pipeline.Prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

# Define the home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Validate and convert form data to CustomData object
            data = CustomData(
                age=request.form.get("age"),
                sex=request.form.get("sex"),
                cp=(request.form.get("cp")),
                trestbps=(request.form.get("trestbps")),
                chol=(request.form.get("chol")),
                fbs=request.form.get("fbs"),
                restecg=request.form.get("restecg"),
                thalach=(request.form.get("thalach")),
                exang=request.form.get("exang"),
                oldpeak=request.form.get("oldpeak"),
                slope=request.form.get("slope"),
                ca=request.form.get("ca"),
                thal=(request.form.get("thal"))
            )

            final_data = data.get_data_as_dataframe()
            # Make prediction
            predict_pipeline = PredictPipeline()
            pred = predict_pipeline.predict(final_data)
            result = round(pred[0], 2)
            return render_template("result.html", final_result=result)

        except Exception as e:
            # Handle exceptions gracefully
            error_message = f"Error during prediction: {str(e)}"
            return render_template("error.html", error_message=error_message)

    else:
        # Render the initial page
        return render_template("index.html")

# Execution begins
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
