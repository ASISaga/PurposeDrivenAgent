import azure.functions as func
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from config import MODEL_DIR

# Load the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Extract input from the request
    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get('text')
        except ValueError:
            return func.HttpResponse("Invalid input. Please provide a text input.", status_code=400)

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt")

    # Perform inference using the pre-trained model
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1).item()

    # Return the prediction
    return func.HttpResponse(
        json.dumps({"prediction": predictions}),
        status_code=200,
        mimetype="application/json"
    )
