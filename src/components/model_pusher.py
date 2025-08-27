import os, sys 
from src.cloud_storage.aws_storage import SimpleStorageService 
from src.exception import MyException 
from src.logger import logging 
from src.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact,ModelTrainerArtifact 
from src.entity.config_entity import ModelPusherConfig 
from src.entity.s3_estimator import Proj1Estimator 

class ModelPusher:
    def __init__(self, model_evaluation_artifact=ModelEvaluationArtifact, model_pusher_config=ModelPusherConfig):
        self.s3=SimpleStorageService()
        self.model_evaluation_artifact=model_evaluation_artifact 
        self.model_pusher_config=model_pusher_config
        self.proj1Estimator=Proj1Estimator(bucket_name=model_pusher_config.bucket_name,
                                           model_path=model_pusher_config.s3_model_key_path)
    
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")
        try:
            print("------------------------------------------------------------------------------------------------")
            logging.info("Uploading artifacts folder to s3 bucket")
            
            logging.info("Uploading new model to S3 bucket....")
            self.proj1Estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact=ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                      s3_model_path=self.model_pusher_config.s3_model_key_path)
            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact 
        except Exception as e:
            raise MyException(e,sys) from e 
        
    
        
