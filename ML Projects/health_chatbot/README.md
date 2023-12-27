# Health_Chatbot


## Overview
This repository contains a Python script that fine-tunes a pre-trained LLama2-7B-Chat model using Lora and PEFT (Post-Training) techniques. The script leverages the power of LLama2-7B-Chat, and enhances its capabilities through quantization and other optimizations.

## Repository Structure
- **model:** Contains saved checkpoint files of the pre-trained LLama2-7B-Chat model.
- **src:** Includes scripts for different purposes:
  - `main.py`: Script for fine-tuning the LLama2-7B-Chat model.
- **notebook:** Notebooks for analysis and development.
- `README.md`: Information about the repository.

## Usage
- **Fine-Tuning:** Run `main.py` to fine-tune the LLama2-7B-Chat model. Ensure necessary dependencies are installed as specified in the README.

## Getting Started
1. Clone this repository.
2. Install the required dependencies using `pip install torch torch.nn transformers peft trl`.
3. Load the pre-trained LLama2-7B-Chat model HuggingFace Hub.
4. Execute the `main.py` script to fine-tune the model.

## Model Architecture and Optimizations
The script fine-tunes the LLama2-7B-Chat model using the following techniques:
- Quantization
- Lora
- PEFT

## Training and Evaluation
The script utilizes the `SFTTrainer` class from the `trl` library to train the model with specified hyperparameters.

## Results and Performance
The fine-tuned model's performance is evaluated using a dataset from HuggingFaceHub.

## Contributing and Support
Contributions and support are welcome! Feel free to open an issue or submit a pull request for any questions or assistance.

## License
This project is licensed under the MIT License.

