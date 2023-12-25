
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM,GPTQConfig, TrainingArguments
from peft import LoraConfig,prepare_model_for_kbit_training, get_peft_model
from trl import SFTTrainer
dataset = load_dataset("DR-DRR/Medical_Customer_care",split='train')

def main():
  model_ckpt = "TheBloke/Llama-2-7b-Chat-GPTQ"

  tokenizer = AutoTokenizer.from_pretrained(
      model_ckpt
  )
  tokenizer.pad_token = tokenizer.eos_token
  quantization_config = GPTQConfig(bits=4,disable_exllama=True,tokenizer=tokenizer)
  model = AutoModelForCausalLM.from_pretrained(
      model_ckpt,
      revision='main',
      quantization_config=quantization_config,
      device_map='auto')
  model.config.use_cache = False
  model.config.pretraining_tp = 1
  model.gradient_checkpointing_enable()
  model = prepare_model_for_kbit_training(model)

  lora_config = LoraConfig(r=16,
                          lora_alpha=32,
                          lora_dropout=0.05,
                          bias='none',
                          task_type='CAUSAL_LM',
                          target_modules=[
                                      "q_proj",
                                      "k_proj",
                                      "v_proj",
                                      "o_proj",
                                      "gate_proj",
                                      "up_proj",
                                      "down_proj",
                                          ]
  )
  model = get_peft_model(model,lora_config)

  training_args = TrainingArguments(output_dir='.',
                                 dataloader_drop_last=True,
                                 save_strategy='epoch',
                                 num_train_epochs=1,
                                 logging_steps=100,
                                 max_steps=2000,
                                 per_device_train_batch_size=1,
                                 learning_rate=3e-4,
                                 lr_scheduler_type='cosine',
                                 warmup_steps=100,
                                 fp16=True,
                                 weight_decay=0.05,
                                 report_to=None,
                                 run_name='finetuning-llama2-chat-7b')
  trainer = SFTTrainer(model=model,
                    args=training_args,
                    train_dataset = dataset,
                    dataset_text_field='text',
                    max_seq_length=1024,
                    tokenizer=tokenizer,
                    packing=False)
  trainer.train()

if __name__ == "__main__":
  main()
