from datasets import load_dataset

def get_data():
    dataset = load_dataset("multi_news")
    return dataset