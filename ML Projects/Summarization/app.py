import streamlit as st
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the fine-tuned T5 model and tokenizer
model_path = "Neupane9Sujal/Text_Summarization"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Function to generate summaries
def generate_summary(text):
    # Tokenize input text
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True).to(device)
    #st.write(inputs.shape)
    # Generate summary
    summary_ids = model.generate(inputs, num_beams=4, max_length=264, early_stopping=True)
    summary = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    
    return summary

# Streamlit app
def main():
    st.title("Text Summarization")

    # User input
    user_input = st.text_area("Enter the text to summarize")

    # Generate summary button
    if st.button("Generate Summary"):
        if user_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            # Generate summary
            summary = generate_summary(user_input)
            
            # Display summary
            st.subheader("Summary")
            st.write(summary)

if __name__ == "__main__":
    main()
