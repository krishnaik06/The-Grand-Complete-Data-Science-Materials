import os
from Indian_Coin_Detection import logger
from Indian_Coin_Detection.entity.config_entity import DataValidationConfig

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_all_files_exist(self)-> bool:
        logger.info(f"Starting Data Validation")
        validation_status = False
        try:
            os.makedirs(self.config.root_dir, exist_ok=True)

            folders1 = os.listdir(self.config.unzip_data_dir)

            all_req_folder_present = True
            for folder1 in self.config.data_validation_req_dir_1:
                if folder1 not in folders1:
                    all_req_folder_present = False
                    break

                sub_dir_2 = os.path.join(self.config.unzip_data_dir,folder1)
                folders2 = os.listdir(sub_dir_2)
                for folder2 in self.config.data_validation_req_dir_2:
                    if folder2 not in folders2:
                        all_req_folder_present = False
                        break

            if all_req_folder_present == True:
                if os.path.isfile(self.config.yolo_config_file_path):
                    validation_status = True


        except Exception as e:
            raise e
        logger.info(f"Validation Status is {validation_status}")
        with open(self.config.STATUS_FILE, 'w') as f:
            f.write(f"Validation status: {validation_status}")
        return validation_status