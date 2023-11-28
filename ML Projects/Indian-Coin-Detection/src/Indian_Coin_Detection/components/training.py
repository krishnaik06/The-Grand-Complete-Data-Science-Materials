import os
from pathlib import Path
import shutil
from ultralytics import YOLO
from Indian_Coin_Detection.entity.config_entity import TrainingConfig

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    @staticmethod
    def save_weights(temp_weights_path: str,store_weights_path: Path):
    
        shutil.copyfile(temp_weights_path, store_weights_path)

    def train(self):
        model = YOLO("yolov8n.yaml")
        model = YOLO("yolov8n.pt")

        results = model.train(data=self.config.yolo_config_file_path, 
                              epochs = self.config.params_epochs,
                              imgsz = self.config.params_image_size,
                              project = self.config.trained_model_dir)
        
        # temp_best_weights_path = "/home/debasish/home/Indian-Coin-Detection/runs/detect/train2/weights/best.pt"
        # temp_last_weights_path = "/home/debasish/home/Indian-Coin-Detection/runs/detect/train2/weights/last.pt"
        
        # self.save_weights(temp_best_weights_path,self.config.best_weight_path)
        # self.save_weights(temp_last_weights_path,self.config.last_weight_path)