from flask import Flask, render_template, url_for, redirect, request, session
import pandas as pd
import numpy as np
from dotenv import dotenv_values

APP_SECRET = dotenv_values()

app = Flask(__name__, template_folder='templates')
app.secret_key = APP_SECRET['SECRET_KEY_FLASK']

bike = pd.read_pickle('data/bikes_v4.pkl')
bike_names = bike['model'].unique()

   
bajaj_motorbike = "https://seeklogo.com/images/B/bajaj-motorcycle-logo-AF3E4F0857-seeklogo.com.png"

royal_enfield_motorbike = "https://seeklogo.com/images/R/royal-enfield-logo-939DEE699F-seeklogo.com.png"

hyosung_motorbike = "https://seeklogo.com/images/H/hyosung-logo-DDF6E9415C-seeklogo.com.png"

ktm_motorbike = "https://seeklogo.com/images/K/ktm-logo-5F046681E7-seeklogo.com.png"

tvs_motorbike = "https://seeklogo.com/images/T/tvs-motor-company-logo-64528DF51C-seeklogo.com.png"

yamaha_motorbike = "https://seeklogo.com/images/Y/yamaha-logo-78357B8991-seeklogo.com.png"

honda_motorbike = "https://seeklogo.com/images/H/honda-logo-48963B6E1F-seeklogo.com.png"

um_motorbike = "https://seeklogo.com/images/U/um-logo-92833D2706-seeklogo.com.png"

hero_motorbike = "https://seeklogo.com/images/H/hero-logo-BED9024F3F-seeklogo.com.png"

suzuki_motorbike = "https://seeklogo.com/images/S/Suzuki-logo-1298046A2E-seeklogo.com.png"

husqvarna_motorbike = "https://seeklogo.com/images/H/Husqvarna-logo-D996C98848-seeklogo.com.png"

mahindra_motorbike = "https://seeklogo.com/images/M/mahindra-logo-F6291B6661-seeklogo.com.png"

harley_davidson_motorbike = "https://seeklogo.com/images/H/Harley-Davidson-logo-86593F6887-seeklogo.com.png"

kawasaki_motorbike = "https://seeklogo.com/images/K/Kawasaki-logo-323EEAD330-seeklogo.com.png"

triumph_motorbike = "https://seeklogo.com/images/T/triumph-logo-FAEB5DC5C3-seeklogo.com.png"

ducati_motorbike = "https://seeklogo.com/images/D/ducati-logo-3000A98790-seeklogo.com.png"

benelli_motorbike = "https://seeklogo.com/images/B/Benelli-logo-E959D41F7A-seeklogo.com.png"

moto_guzzi_motorbike = "https://seeklogo.com/images/M/Moto_Guzzi-logo-77E7FD7F3D-seeklogo.com.png"

indian_motorbike = "https://seeklogo.com/images/I/Indian_Motorcycle-logo-E5EAF58AEE-seeklogo.com.png"

aprilia_motorbike = "https://seeklogo.com/images/A/Aprilia-logo-A91BD1252A-seeklogo.com.png"

mv_motorbike = "https://seeklogo.com/images/M/mv-agusta-logo-97CBCABE6F-seeklogo.com.png"


image_links = [
    bajaj_motorbike,
    royal_enfield_motorbike,
    hyosung_motorbike,
    ktm_motorbike,
    tvs_motorbike,
    yamaha_motorbike,
    honda_motorbike,
    um_motorbike,
    hero_motorbike,
    suzuki_motorbike,
    husqvarna_motorbike,
    mahindra_motorbike,
    harley_davidson_motorbike,
    kawasaki_motorbike,
    triumph_motorbike,
    ducati_motorbike,
    benelli_motorbike,
    moto_guzzi_motorbike,
    indian_motorbike,
    aprilia_motorbike,
    mv_motorbike
]

bike_info = dict()
for bike_name, bike_logo in zip(bike_names, image_links):
    bike_info[bike_name] = bike_logo




luxurycar_brands = ['Volkswagen', 'Audi', 'Jeep', 'Skoda', 'Bmw', 'Peugeot', 'Ford',
       'Mazda', 'Nissan', 'Renault', 'Mercedesbenz', 'Opel', 'Seat',
       'Citroen', 'Honda', 'Fiat', 'Mini', 'Smart', 'Hyundai',
         'Alfaromeo', 'Subaru', 'Volvo', 'Mitsubishi',
       'Kia', 'Suzuki', 'Lancia', 'Porsche', 'Toyota', 'Chevrolet',
       'Dacia', 'Daihatsu', 'Trabant', 'Saab', 'Chrysler', 'Jaguar',
       'Daewoo', 'Rover', 'Landrover', 'Lada']

Volkswagen = 'https://seeklogo.com/images/V/Volkswagen-logo-FAE94F013E-seeklogo.com.png'

Audi = 'https://seeklogo.com/images/A/Audi-logo-70A7072C07-seeklogo.com.png'

Jeep = 'https://seeklogo.com/images/J/Jeep-logo-95D59945A7-seeklogo.com.png'

Skoda = 'https://seeklogo.com/images/S/skoda-logo-603B0DB338-seeklogo.com.png'

Bmw = 'https://seeklogo.com/images/B/bmw-logo-248C3D90E6-seeklogo.com.png'

Peugeot = 'https://seeklogo.com/images/P/peugeot-new-2021-logo-8E83714E02-seeklogo.com.png'

Ford = 'https://seeklogo.com/images/F/ford-logo-CA98E97A2B-seeklogo.com.png'

Mazda='https://seeklogo.com/images/M/Mazda-logo-CC1CF9FB16-seeklogo.com.png'

Nissan='https://seeklogo.com/images/N/Nissan-logo-4B3C580C8A-seeklogo.com.png'

Renault='https://seeklogo.com/images/R/renault-logo-189254C54A-seeklogo.com.png'

Mercedesbenz='https://seeklogo.com/images/M/mercedes-benz-logo-B29195852E-seeklogo.com.png'

Opel='https://seeklogo.com/images/O/opel-new-logo-D9A5129C2D-seeklogo.com.png'

Seat='https://seeklogo.com/images/S/Seat-logo-3EE562BF78-seeklogo.com.png'

Citroen='https://seeklogo.com/images/C/citroen-2009-logo-456E9DFB33-seeklogo.com.png'

Honda='https://seeklogo.com/images/H/honda-logo-CA469AE008-seeklogo.com.png'

Fiat='https://seeklogo.com/images/F/FIAT_2007_OLD-logo-4195DE7DDB-seeklogo.com.png'

Mini='https://seeklogo.com/images/M/mini-cooper-logo-2B30B836FE-seeklogo.com.png'

Smart='https://seeklogo.com/images/S/smart-logo-0F77F63B9D-seeklogo.com.png'

Hyundai='https://seeklogo.com/images/H/hyundai-logo-50C0EC8456-seeklogo.com.png'

Alfaromeo='https://seeklogo.com/images/A/alfa-romeo-logo-FE33086493-seeklogo.com.png'

Subaru='https://seeklogo.com/images/S/subaru-logo-E7467F601A-seeklogo.com.png'

Volvo='https://seeklogo.com/images/V/Volvo-logo-C760DE2579-seeklogo.com.png'

Mitsubishi='https://seeklogo.com/images/M/mitsubishi-logo-67EA251D5A-seeklogo.com.png'

Kia='https://seeklogo.com/images/K/kia-new-2021-logo-BBE1BFFF1A-seeklogo.com.png'

Suzuki='https://seeklogo.com/images/S/suzuki-logo-5311518DD9-seeklogo.com.png'

Lancia='https://seeklogo.com/images/L/lancia_2007-logo-A0283C7FF5-seeklogo.com.png'

Porsche='https://seeklogo.com/images/P/porsche-logo-5995000C95-seeklogo.com.png'

Toyota='https://seeklogo.com/images/T/toyota-logo-239F6C9C1A-seeklogo.com.png'

Chevrolet='https://seeklogo.com/images/C/CHEVROLET-logo-D2D04ACB9A-seeklogo.com.png'

Dacia='https://seeklogo.com/images/D/dacia-new-2021-logo-F7FCF9412B-seeklogo.com.png'

Daihatsu='https://seeklogo.com/images/D/daihatsu-logo-A6249D607C-seeklogo.com.png'

Trabant='https://seeklogo.com/images/T/Trabant-logo-449EB9F9B1-seeklogo.com.png'

Saab='https://seeklogo.com/images/S/Saab_MY2001-logo-3682B9389D-seeklogo.com.png'

Chrysler='https://seeklogo.com/images/C/Chrysler-logo-5837FDA753-seeklogo.com.png'

Jaguar='https://seeklogo.com/images/J/Jaguar-logo-ED7E01A4A1-seeklogo.com.png'

Daewoo='https://seeklogo.com/images/D/Daewoo-logo-058F288C41-seeklogo.com.png'

Rover='https://seeklogo.com/images/R/range-rover-logo-B486481AE8-seeklogo.com.png'

Landrover='https://seeklogo.com/images/L/land-rover-logo-86296C9BE7-seeklogo.com.png'

Lada='https://seeklogo.com/images/L/lada-logo-EDBC91BA94-seeklogo.com.png'


luxury_car_logos = [Volkswagen, Audi, Jeep, Skoda, Bmw, Peugeot, Ford, Mazda, Nissan, Renault, Mercedesbenz, Opel, Seat, Citroen, Honda, Fiat, Mini, Smart, Hyundai, Alfaromeo, Subaru, Volvo, Mitsubishi, Kia, Suzuki, Lancia, Porsche, Toyota, Chevrolet, Dacia, Daihatsu, Trabant, Saab, Chrysler, Jaguar, Daewoo, Rover, Landrover, Lada]

luxucy_car_info = dict()
for luxucy_car_name, luxucy_car_logo in zip(luxurycar_brands, luxury_car_logos):
    luxucy_car_info[luxucy_car_name] = luxucy_car_logo




indiancar_brands = ['Hyundai', 'Mahindra', 'Ford', 'Maruti', 'Skoda', 'Audi', 'Toyota','Renault', 'Honda', 'Datsun', 'Mitsubishi', 'Tata', 'Volkswagen',
       'Chevrolet', 'Mini', 'BMW', 'Nissan', 'Hindustan', 'Fiat', 'Force',
       'Mercedes', 'Land', 'Jaguar', 'Jeep', 'Volvo']

Mahindra = 'https://seeklogo.com/images/M/mahindra-suvs-logo-AAF596FF12-seeklogo.com.png'

Maruti = 'https://seeklogo.com/images/M/maruti-logo-1E67E17B04-seeklogo.com.png'

Datsun= 'https://seeklogo.com/images/D/datsun-logo-562CCF38B8-seeklogo.com.png'

Tata = 'https://seeklogo.com/images/T/TATA-logo-B17191F4CA-seeklogo.com.png'

Hindustan = 'https://seeklogo.com/images/H/hindustan-motors-logo-408ABFA9E7-seeklogo.com.png'

Force = 'https://seeklogo.com/images/F/force-motors-logo-4BCE9AAB19-seeklogo.com.png'


indian_car_logos = [Hyundai, Mahindra, Ford, Maruti, Skoda, Audi, Toyota, Renault, Honda, Datsun, Mitsubishi, Tata, Volkswagen, Chevrolet, Mini, Bmw, Nissan, Hindustan, Fiat, Force, Mercedesbenz, Landrover, Jaguar, Jeep, Volvo]

indian_car_info = dict()
for indian_car_name, indian_car_logo in zip(indiancar_brands, indian_car_logos):
    indian_car_info[indian_car_name] = indian_car_logo



@app.route('/')
def index():
    return redirect(url_for('home'))

image = 'https://cdn.pixabay.com/photo/2023/07/30/11/51/automobile-8158723_1280.jpg'

@app.route('/home')
def home():
    session.clear()
    return render_template('index.html', image=image)

@app.route('/car')
def car():
    session.clear()
    return render_template('car.html')

@app.route('/motorbike')
def motorbike():
    session.clear()
    return render_template('motorbike.html', zipped = bike_info)

@app.route('/luxurycars')
def luxurycar():
    session.clear()
    return render_template('luxury_car.html', zipped=luxucy_car_info)

@app.route('/luxurycarnames', methods=['POST', 'GET'])
def getLuxuryNames():
    session.pop('luxurycar_model_name', None)
    if request.method == 'POST':
        model = request.form.get('model')
        session['luxurycar_model_name'] = model
        
        luxurycar = pd.read_pickle('data/german_car.pkl')
        luxurycar_names = luxurycar[luxurycar['brand']==str(model)]['name'].unique()
        return render_template('luxury_car_names.html',
                                luxurycar_models=luxurycar_names,
                                model_name = model,
                                model_logo = luxucy_car_info[model])
    else:
        
        pass



@app.route('/luxurycarfeatures', methods=['POST', 'GET'])
def getLuxuryFeatures():
    if request.method == 'POST':
        car_name = request.form.get('car_model')
        session['luxurycar_name'] = car_name
        model = session['luxurycar_model_name']
        luxurycar = pd.read_pickle('data/german_car.pkl')
        luxurycar_vehicle_type = luxurycar[luxurycar['name']==str(car_name)]['vehicleType'].unique()
        luxurycar_gearbox = luxurycar[luxurycar['name']==str(car_name)]['gearbox'].unique()
        luxurycar_fueltype = luxurycar[luxurycar['name']==str(car_name)]['fuelType'].unique()
        return render_template('luxury_car_features.html',
                                luxurycar_vehicle_type = luxurycar_vehicle_type,
                                luxurycar_gearbox = luxurycar_gearbox,
                                luxurycar_fueltype=luxurycar_fueltype,
                                model_name = model,
                                model_logo = luxucy_car_info[model])
    else:
        
        pass

@app.route('/indiancars')
def indiancar():
    session.clear()
    return render_template('indian_car.html', zipped=indian_car_info)

@app.route('/indiancarnames', methods=['POST', 'GET'])
def getindianNames():
    session.pop('indiancar_model_name', None)
    if request.method == 'POST':        
        model = request.form.get('model')
        session['indiancar_model_name'] = model
        
        indiancar = pd.read_csv('data/indian_car.csv')
        indiancar_names = indiancar[indiancar['company']==str(model)]['name'].unique()
        return render_template('indian_car_names.html',
                                indiancar_models=indiancar_names,
                                model_name = model,
                                model_logo = indian_car_info[model])
    else:
        
        pass



@app.route('/indiancarfeatures', methods=['POST', 'GET'])
def getindianFeatures():
    if request.method == 'POST':
        car_name = request.form.get('car_model')
        session['indiancar_name'] = car_name
        model = session['indiancar_model_name']
        indiancar = pd.read_csv('data/indian_car.csv')
        indiancar_fueltype = indiancar[indiancar['name']==str(car_name)]['fuel_type'].unique()
        return render_template('indian_car_features.html',
                                indiancar_fueltype=indiancar_fueltype,
                                model_name = model,
                                model_logo = indian_car_info[model])
    else:
        
        pass


@app.route('/bikename', methods=['POST', 'GET'])
def getBikeName():
    session.pop('bike_model_name', None)
    if request.method == 'POST':
        model = request.form.get('model')
        session['bike_model_name'] = model
        
        bike = pd.read_pickle('data/bikes_v4.pkl')
        bike_names = bike[bike['model']==str(model)]['name'].unique()
        return render_template('motorbike_names.html',
                                bike_models=bike_names,
                                model_name = model,
                                model_logo = bike_info[model])
    else:
        
        pass
    


@app.route('/bikefeatures', methods=['POST', 'GET'])
def getBikeFeatures():
    if request.method == 'POST':
        bike_name = request.form.get('bike_model')
        session['bike_name'] = bike_name
        model = session['bike_model_name']
        bike = pd.read_pickle('data/bikes_v4.pkl')
        owner_type = sorted(bike[bike['name']==str(bike_name)]['owner'].unique())
        return render_template('motorbike_features.html',
                                owner_type = owner_type,
                                model_name = model,
                                model_logo = bike_info[model])
    else:
        
        pass

@app.route('/price', methods=['POST', 'GET'])
def getPrice():
    if request.method == 'POST':
        if 'bike_model_name' in session:
            import skops.io as sio
            bikepipe = sio.load('models/indianbikemodel_pipeline.skops',trusted=True)

            model = session['bike_model_name']
            bike_name = session['bike_name']
            owner_type = request.form.get('owner_type')
            model_year = request.form.get('model_year')
            km_driven = request.form.get('km_driven')
            mileage = bike[bike['model']==str(model)]['mileage(kmpl)'].unique()[0]
            price = bikepipe.predict(pd.DataFrame([[model_year,owner_type,bike_name, model, km_driven, mileage]], columns=['model_year', 'owner', 'name', 'model', 'km_driven', 'mileage(kmpl)']))


            return render_template('priceresult.html', 
                                vehicle_name = bike_name, 
                                model_year = model_year,
                                km_driven = km_driven,
                                lowprice=np.ceil(((price)**2-(((price)**2)*0.2))), 
                                highprice=np.ceil(((price)**2+(((price)**2)*0.2))))
        
            
        if 'luxurycar_model_name' in session:
            import skops.io as sio
            luxurycarpipe = sio.load('models/carmodel.skops',trusted=True)

            model = session['luxurycar_model_name']
            luxurycar_name = session['luxurycar_name']
            luxuryvehicletype = request.form.get('luxurycar_vehicle_type')
            luxurygearbox = request.form.get('luxurycar_gearbox')
            fueltype = request.form.get('luxurycar_fueltype')
            model_year = request.form.get('model_year')
            km_driven = request.form.get('km_driven')
            notrepeareddamage = request.form.get('notRepairedDamage')
            price = luxurycarpipe.predict(pd.DataFrame([[luxurycar_name, luxuryvehicletype, model_year, luxurygearbox,km_driven, fueltype, model, notrepeareddamage]], columns=['name', 'vehicleType', 'yearOfRegistration', 'gearbox', 'kilometer','fuelType', 'brand', 'notRepairedDamage']))


            return render_template('priceresult.html', 
                                vehicle_name = luxurycar_name, 
                                model_year = model_year,
                                km_driven = km_driven,
                                lowprice=price-(price*0.20), 
                                highprice=price+(price*0.20))
        


        if 'indiancar_model_name' in session:
            import skops.io as sio
            indiancarpipe = sio.load('models/indiancarmodel_pipeline.skops',trusted=True)

            model = session['indiancar_model_name']
            indiancar_name = session['indiancar_name']
            fueltype = request.form.get('indiancar_fueltype')
            model_year = request.form.get('model_year')
            km_driven = request.form.get('km_driven')
            price = indiancarpipe.predict(pd.DataFrame([[indiancar_name, model, model_year, km_driven, fueltype]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))


            return render_template('priceresult.html', 
                                vehicle_name = indiancar_name, 
                                model_year = model_year,
                                km_driven = km_driven,
                                lowprice=price-(price*0.20), 
                                highprice=price+(price*0.20))
        else:
            pass



@app.route('/features')
def features():
    return render_template('features.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)