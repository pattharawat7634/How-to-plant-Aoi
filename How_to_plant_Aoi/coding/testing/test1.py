import tensorflow as tf
from transformers import BertTokenizer, TFBertForQuestionAnswering
import numpy as np

# Load pre-trained model and tokenizer
model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = TFBertForQuestionAnswering.from_pretrained(model_name)

def answer_question(context, question):
    # Tokenize input
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="tf")
    
    # Get model prediction
    outputs = model(inputs)
    
    # Process the output
    answer_start = tf.argmax(outputs.start_logits, axis=1).numpy()[0]
    answer_end = tf.argmax(outputs.end_logits, axis=1).numpy()[0] + 1
    
    # Convert token indices to actual text
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))
    
    return answer

# Example usage
context = "TensorFlow is an open-source machine learning framework developed by Google. It is widely used for various AI applications including natural language processing and computer vision."
question = "Who developed TensorFlow?"

answer = answer_question(context, question)
print(f"Question: {question}")
print(f"Answer: {answer}")