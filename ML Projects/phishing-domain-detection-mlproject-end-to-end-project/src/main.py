import os
from wsgiref import simple_server
from flask import Flask, request, render_template, jsonify
from flask import Response
from flask_cors import CORS, cross_origin
from src.ML_pipelines.stage_03_prediction import prediction
import pickle
# os.putenv('LANG', 'en_US.UTF-8')
# os.putenv('LC_ALL', 'en_US.UTF-8')
from src.training_Validation_Insertion import train_validation

app = Flask(__name__)
# dashboard.bind(app)
CORS(app)
filename = "XGBoost.pkl"
model = pickle.load(open(filename, 'rb'))

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    try:
        #Getting user input details
        # qty_slash_url = request.json["qty_slash_url"]
        qty_slash_url = request.form.get("qty_slash_url")
        # length_url = request.json["length_url"]
        length_url = request.form.get("length_url")
        # qty_dot_domain = request.json["qty_dot_domain"]
        qty_dot_domain = request.form.get("qty_dot_domain")
        # qty_dot_directory = request.json["qty_dot_directory"]
        qty_dot_directory = request.form.get("qty_dot_directory")
        #qty_hyphen_directory = request.json["qty_hyphen_directory"]
        qty_hyphen_directory = request.form.get("qty_hyphen_directory")
        #file_length = request.json["file_length"]
        file_length = request.form.get("file_length")
        #qty_underline_directory = request.json["qty_underline_directory"]
        qty_underline_directory = request.form.get("qty_underline_directory")
        # asn_ip = request.json["asn_ip"]
        asn_ip = request.form.get("asn_ip")
        #time_domain_activation = request.json["time_domain_activation"]
        time_domain_activation = request.form.get("time_domain_activation")
        #time_domain_expiration = request.json["time_domain_expiration"]
        time_domain_expiration = request.form.get("time_domain_expiration")
        #ttl_hostname = request.json["ttl_hostname"]
        ttl_hostname = request.form.get("ttl_hostname")
        result=prediction(qty_slash_url,length_url,qty_dot_domain,qty_dot_directory,qty_hyphen_directory,file_length,
                              qty_underline_directory,asn_ip,time_domain_activation,time_domain_expiration,ttl_hostname,
                          model)
        #print(result)
        result1 = "malicious" if result==1 else "legitimate"
        r =Response(response=result1, status=200,mimetype='application/json')
        return render_template("index.html",prediction_text="{}".format(result1))
        # return r
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def train():
    try:
        path = os.path.join("data/", "raw/")
        train_valObj = train_validation(path)  # object initialization
        train_valObj.train_validation()  # calling the training_validation function
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    app.debug=True
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()

