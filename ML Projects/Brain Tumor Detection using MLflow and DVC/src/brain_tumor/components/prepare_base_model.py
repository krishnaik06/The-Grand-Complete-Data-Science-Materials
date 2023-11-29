
import os
import urllib.request as request 
from zipfile import ZipFile
import tensorflow as tf
from brain_tumor.entity.config_entity import PrepareBaseModelConfig
from pathlib import Path 


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config 


    def get_base_model(self):
        self.model = tf.keras.applications.resnet50.ResNet50(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        self.save_model(path=self.config.base_model_path, model=self.model)


    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False

        
        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(flatten_in)


        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )


        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        full_model.summary()
        return full_model
    

    def updated_base_model(self):
        self.full_model = self._prepare_full_model(
            model = self.model,
            classes = self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate
        )


        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)


    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)