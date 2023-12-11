from transformers import Trainer, TrainingArguments, T5ForConditionalGeneration

def train_model(tok_ds,num_train_epochs,batch_size):
    model = T5ForConditionalGeneration.from_pretrained('t5-base')
    training_args = TrainingArguments(
    output_dir="./output",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    save_total_limit=2,
    num_train_epochs=num_train_epochs,
    save_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    fp16=True
    )
    trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tok_ds["train"],
    eval_dataset=tok_ds["validation"],
    #data_collator=data_collator,
    compute_metrics=lambda p: compute_rouge_scores(
        tokenizer.batch_decode(p.predictions, skip_special_tokens=True),
        tokenizer.batch_decode(p.label_ids, skip_special_tokens=True),
        ),
    )
    trainer.train()
    return trainer