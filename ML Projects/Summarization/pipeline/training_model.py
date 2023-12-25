from steps.preprocess import preprocess
from steps.model_train import train_model
from steps.evaluation import evaluate_model
from pipeline.inference_pipeline import infer_model


def training_pipeline(num_train_epochs,batch_size):
    tok_ds = preprocess()
    #data_collator = DataCollatorForSeq2Seq(tokenizer,model=model,return_tensors='pt')
    trainer = train_model(tok_ds, num_train_epochs, batch_size)
    trained_model = trainer.model
    eval_metric = evaluate_model(trainer)
    infer_model(trainer)
