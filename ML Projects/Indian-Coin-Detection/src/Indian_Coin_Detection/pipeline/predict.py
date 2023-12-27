import numpy as np
import os
from ultralytics import YOLO
import cv2
from Indian_Coin_Detection import logger
import cv2 as cv

from Indian_Coin_Detection import logger



class PredictionPipeline:
    def __init__(self,filename:str,model_type:str,threshold:float):
        self.filename = filename
        self.model_type = model_type
        self.threshold = threshold

    def write_label_bounding_box(self,result,img, class_id, x1, y1, x2, y2, score):
        score_str = 'Score: {:.2f}'.format(score)
        class_name = result.names[int(class_id)].replace("₹", "")
        text = class_name + ' ' + score_str
        
        if class_id == 0:
            color = (255, 128, 0)
        elif class_id == 1:
            color = (0, 165, 255)
        elif class_id == 2:
            color = (147, 20, 255)
        elif class_id == 3:
            color = (255, 0, 255)
        else:
            color = (0, 0, 0)  # Default color
        
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 20)
        cv2.putText(img, text, (int(x1), int(y1 - 30)), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 20, cv2.LINE_AA)
        
        return img
    
    def get_prediction_data(self,result,img,threshold):
        #threshold = 65
        output = {}
        output['₹1'],output['₹2'],output['₹5'],output['₹10'] = 0,0,0,0

        for i in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = i
            if score >= threshold:
                #print(score,class_id,threshold)
                pred_class = result.names[class_id]

                output[pred_class] += 1
                img = self.write_label_bounding_box(result,img,class_id,x1, y1, x2, y2,score)

        return img,output

    
    def predict(self):
        # load model

        if self.model_type == 'yolo-medium':
            model_path = os.path.join(
                "artifacts", "training", "model", "yolo-medium", "train", "weights", "best.pt")
        elif self.model_type == 'yolo-small':
            model_path = os.path.join(
                "artifacts", "training", "model", "yolo-small", "train", "weights", "best.pt")
        elif self.model_type == 'yolo-nano':
            model_path = os.path.join(
                "artifacts", "training", "model", "yolo-nano", "train", "weights", "best.pt")
        else:
            model_path = os.path.join(
                "artifacts", "training", "model", "temporary_model", "train", "weights", "best.pt")

        model = YOLO(model_path)
        img_path = self.filename
        results = model(img_path)
        result = results[0]

        img = cv.imread(img_path, cv.IMREAD_UNCHANGED)

        output_img,output_data = self.get_prediction_data(result,img,self.threshold)

        scale_percent = 50 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized_output_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        # cv2.imwrite('temp1.jpg',resized_output_img)
        # cv2.imwrite('temp2.jpg',output_img)

        total_amount = (output_data['₹1'])+(2*output_data['₹2'])+(5*output_data['₹5'])+(10*output_data['₹10'])

        prediction = { "number of ₹1" : output_data["₹1"],
                        "number of ₹2" : output_data["₹2"],
                        "number of ₹5" : output_data["₹5"],
                        "number of ₹10" : output_data["₹10"],
                        "Total Amount" : '₹'+str(total_amount)
                        }

        #prediction = len(result.boxes)
        #return [{ "image" : prediction}]

        return prediction,resized_output_img

    
STAGE_NAME = "Prediction"
if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        image_filename = ''
        model_type = ''
        threshold = 0
        obj = PredictionPipeline(image_filename,model_type=model_type,threshold=threshold)
        obj.predict()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e