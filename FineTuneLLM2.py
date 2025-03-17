# Fine-Tune DeepSeek R1 Distilled Model
# Gather domain-specific text relevant to your tasks (e.g., industry reports, technical documents).
# Clean and format the text. You can split your text into smaller chunks if needed.

# Iterative Fine-Tuning 
# Start with a Small Subset:** Select a small subset of your domain-specific text for the initial fine-tuning.
# Fine-Tune the Model:** Fine-tune the model on this subset and save the intermediate model.

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# Import necessary libraries from the transformers and datasets packages
import transformers
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import Dataset
import faiss  # FAISS library for efficient similarity search

# Define the DocumentTrainer class
class DocumentTrainer:
    def __init__(self, model_name="deepseek-ai/DeepSeek-R1", output_dir="./results"):
        """
        Initialize the DocumentTrainer with the specified model and output directory.
        Args:
            model_name (str): The name of the pretrained model to use.
            output_dir (str): The directory to save training outputs.
        """
        # Initialize the model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Define training arguments for Seq2SeqTrainer
        self.training_args = Seq2SeqTrainingArguments(
            output_dir=output_dir,               # Directory to save training outputs
            evaluation_strategy="epoch",         # Evaluate the model at the end of each epoch
            learning_rate=5e-5,                  # Learning rate for training
            per_device_train_batch_size=4,       # Batch size for training
            per_device_eval_batch_size=4,        # Batch size for evaluation
            weight_decay=0.01,                   # Weight decay to prevent overfitting
            save_total_limit=3,                  # Limit the total number of saved checkpoints
            num_train_epochs=3,                  # Number of training epochs
            predict_with_generate=True,          # Enable text generation during evaluation
        )
        
        # Initialize an empty dataset to store combined documents
        self.combined_dataset = None

    def preprocess_function(self, document):
        """
        Preprocess a document by tokenizing and truncating it to fit the model's input size.
        Args:
            document (str): The document text to preprocess.
        Returns:
            model_inputs (dict): A dictionary containing tokenized inputs.
        """
        model_inputs = self.tokenizer(document, max_length=1024, truncation=True, return_tensors="pt")
        return model_inputs
    
    def add_document_to_dataset(self, document_text):
        """
        Add a new document to the combined dataset.
        Args:
            document_text (str): The document text to add.
        """
        # Preprocess the new document
        tokenized_document = self.preprocess_function(document_text)
        
        # Create a new dataset for the document
        new_dataset = Dataset.from_dict({
            "input_ids": tokenized_document["input_ids"], 
            "attention_mask": tokenized_document["attention_mask"]
        })
        
        # Combine the new dataset with the existing dataset
        if self.combined_dataset is None:
            self.combined_dataset = new_dataset
        else:
            self.combined_dataset = self.combined_dataset.concatenate(new_dataset)
    
    def train(self, document):
        """
        Train the model with the given document by adding it to the combined dataset and refining the model.
        Args:
            document (str): The document text to train on.
        """
        # Add the current document to the combined dataset
        self.add_document_to_dataset(document)
        
        # Create a Seq2SeqTrainer instance with the updated dataset
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.combined_dataset,
            tokenizer=self.tokenizer,
        )
        
        # Train the model on the combined dataset
        trainer.train()
    
    def generate_combined_document(self, documents):
        """
        Generate the final combined document from the list of documents.
        Args:
            documents (list): A list of document texts.
        Returns:
            combined_document (str): The combined document generated by the model.
        """
        # Combine all documents into a single input string
        inputs = self.tokenizer("Combine knowledge from these documents: " + " ".join(documents), return_tensors="pt", max_length=1024, truncation=True)
        
        # Generate the combined document using the model
        outputs = self.model.generate(inputs["input_ids"], max_length=1024, num_beams=5, early_stopping=True)
        
        # Decode the generated output to get the combined document text
        combined_document = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return combined_document

# Example usage
documents = ["First document text...", "Second document text...", "Third document text..."]

# Initialize the DocumentTrainer
trainer = DocumentTrainer()

# Iterate over documents and train incrementally
for doc in documents:
    trainer.train(doc)

# Generate the final combined document
combined_document = trainer.generate_combined_document(documents)
print(combined_document)












# Prepare your initial domain-specific text.
texts = ["Your initial domain-specific text goes here..."]

# Define custom dataset
class DomainDataset(torch.utils.data.Dataset):
    def __init__(self, inputs):
        # Load tokenizer and model
        model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.input_ids = inputs['input_ids']
        self.attention_mask = inputs['attention_mask']

# Define training function. It takes a list of texts as input and fine-tunes the model.
    def train(texts):
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        dataset = DomainDataset(inputs)

        # Set up training arguments
        training_args = TrainingArguments(
            output_dir="./results",
            per_device_train_batch_size=2,
            num_train_epochs=1,  # Start with fewer epochs for initial fine-tuning
            logging_dir="./logs",
        )

        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
        )

        # Fine-tune the model
        trainer.train()

        # Save intermediate model
        model.save_pretrained("./intermediate_model")

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_mask[idx]}




# Progressive Fine-Tuning:
## Gradually Increase Data Size:** Gradually include more domain-specific text in subsequent iterations of fine-tuning.
## Adjust Training Parameters:** Adjust the number of epochs, learning rate, and batch size based on the model’s performance and available resources.

# Load intermediate model and tokenizer
model_name = "./intermediate_model"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare additional domain-specific text
additional_texts = ["More domain-specific text for progressive fine-tuning..."]
inputs = tokenizer(additional_texts, return_tensors="pt", padding=True, truncation=True)

# Define custom dataset
dataset = DomainDataset(inputs)

# Update training arguments
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=2,
    num_train_epochs=2,  # Increase the number of epochs for further fine-tuning
    logging_dir="./logs",
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Continue fine-tuning
trainer.train()

# Save progressively fine-tuned model
model.save_pretrained("./final_model")

# Evaluation and Validation:**
## Evaluate the model’s performance on domain-specific tasks using various metrics.
## Validate the model’s generalization capabilities with unseen text from the domain.

# Deployment and Monitoring:**
## Deploy the progressively fine-tuned model to your desired platform.
## Continuously monitor and update the model based on its performance.