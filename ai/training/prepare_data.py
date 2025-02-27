import requests
from datasets import Dataset
from transformers import GPT2Tokenizer

# Download the Tiny Shakespeare dataset
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
response = requests.get(url)
data = response.text

# Save to file
with open('tiny_shakespeare.txt', 'w') as f:
    pass # f.write(data)

with open('data.txt', 'r') as f: # attendance observations
    data = f.read()

# Load data into a Hugging Face Dataset
raw_data = Dataset.from_dict({'text': [data]})

# Print the first 500 characters
print(raw_data['text'][0][:500])

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

def tokenize_function(examples):
    return tokenizer(examples['text'], return_special_tokens_mask=True)

tokenized_dataset = raw_data.map(
    tokenize_function,
    batched=True,
    num_proc=4,
    remove_columns=["text"]
)

block_size = 128

def group_texts(examples):
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated['input_ids'])
    total_length = (total_length // block_size) * block_size
    result = {
        k: [concatenated[k][i:i + block_size] for i in range(0, total_length, block_size)]
        for k in concatenated.keys()
    }
    result["labels"] = result["input_ids"].copy()
    return result

lm_dataset = tokenized_dataset.map(
    group_texts,
    batched=True,
    num_proc=4,
)

lm_dataset.save_to_disk('lm_dataset')
