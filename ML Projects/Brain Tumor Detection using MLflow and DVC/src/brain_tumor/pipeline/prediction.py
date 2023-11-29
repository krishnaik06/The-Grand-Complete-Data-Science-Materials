import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os


class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename

    
    def predict(self):
        # load model
        model = load_model(os.path.join("final_model", "brain_model.h5"))

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (180, 180))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = np.argmax(model.predict(test_image), axis=1)
        print(result)

        if result[0] == 0:
            prediction = 'Giloma'
            return [{"image" : prediction}]
        elif result[0] == 1:
            prediction = 'Meningioma'
            return [{"image": prediction}]
        elif result[0] == 3:
            prediction = 'Pituitary'
            return [{"image": prediction}]
        else:
            prediction = 'Notumor'
            return [{"image" : prediction}]