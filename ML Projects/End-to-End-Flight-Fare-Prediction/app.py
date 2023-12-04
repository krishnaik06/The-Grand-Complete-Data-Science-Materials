from src.FlightPricePrediction.pipeline.Prediction_pipeline import CustomData,PredictPipeline

from flask import Flask,request,render_template,jsonify


app=Flask(__name__)


@app.route("/",methods=["GET","POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    
    else:
        data=CustomData(
            airline = request.form.get('airline'),
            source_city = request.form.get('source_city'),
            departure_time = request.form.get('departure_time'),
            stops = request.form.get('stops'),
            arrival_time = request.form.get('arrival_time'),
            destination_city = request.form.get('destination_city'),
            classs = request.form.get('classs'),
            duration = float(request.form.get('duration')),
            days_left = int(request.form.get('days_left'))
        )
        # this is my final data
        final_data=data.get_data_as_dataframe()
        
        predict_pipeline=PredictPipeline()
        
        pred=predict_pipeline.predict(final_data)
        
        result=round(pred[0],2)
        
        return render_template("result.html",final_result=result)

#execution begin
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
