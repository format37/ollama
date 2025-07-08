from pydantic import BaseModel, Field
from typing import List
import json

class Feature(BaseModel):
    name: str = Field(..., min_length=1, description="Feature name")
    importance: float = Field(..., ge=0.0, le=1.0, description="Importance value between 0 and 1")
    description: str = Field(..., min_length=1, description="Feature description")

class ProductDescription(BaseModel):
    name: str
    description: str
    price: float
    features: List[Feature] = Field(..., description="List of product features")

from ollama import chat

response = chat(
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant that provides detailed descriptions of products. Always respond with valid JSON containing the actual product information with fields: name, description, price (as numeric value without currency symbol), and features. Features should be an array of objects with importance (float 0-1), name, and description fields.'},
        {'role': 'user', 'content': 'Tell me about product Nvidia RTX 4090. Provide the response as JSON with name, description, price (numeric value only, no dollar sign), and features fields. Include 3-5 key features with importance values between 0 and 1.'},
    ],
    model='mistral-small3.2:24b',
    format='json',
)

# Parse the JSON response and convert to structured object
json_content = response["message"]["content"]
print("Raw JSON content:")
print(json_content)
print("\n" + "="*50 + "\n")

try:
    parsed_data = json.loads(json_content)
    print("Parsed data:")
    print(parsed_data)
    print("\n" + "="*50 + "\n")
    
    product = ProductDescription(**parsed_data)
    
    print("Structured output:")
    print(f"Product Name: {product.name}")
    print(f"Description: {product.description}")
    print(f"Price: ${product.price}")
    print(f"\nFeatures:")
    for i, feature in enumerate(product.features, 1):
        print(f"  {i}. {feature.name} (importance: {feature.importance:.2f})")
        print(f"     {feature.description}")
    print(f"\nAs object: {product}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Received data: {parsed_data}")

print("Done")
