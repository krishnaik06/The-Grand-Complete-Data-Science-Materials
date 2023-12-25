from pipeline.training_model import training_pipeline

if __name__ == "__main__":
    num_train_epochs=3
    batch_size=8
    training_pipeline(num_train_epochs, batch_size)