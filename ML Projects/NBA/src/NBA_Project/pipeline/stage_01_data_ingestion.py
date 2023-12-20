from src.NBA_Project.config.configuration import ConfigurationManager
from src.NBA_Project.components.data_ingestion import DataIngestion
from src.NBA_Project import logger

STAGE_NAME='Data Ingestion Name'


class DataIngestionPipeline:

    def __init__(self):

        pass

    def main(self):

        config=ConfigurationManager()
        data_ingestion_config=config.get_data_ingestion_config()
        data_ingestion=DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()



if __name__=='__main__':

    try:

        logger.info(f">>>>>>>>>>>< stage {STAGE_NAME} stared <<<<<<<<<")

        obj=DataIngestionPipeline()
        obj.main()

        logger.info(f">>>>>>>>>end of {STAGE_NAME}<<<<<<<<<<<<")

    except Exception as e:
        logger.exception(e)
        raise e