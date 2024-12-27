from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

# Load the flow YAML (Image Prompt Generator)
flow = Flow(source="flow-img.yaml")

# Prepare the input dictionary with product details
input_dict = {
    "productName": "SuperWidget",
    "productDescription": "The most advanced widget on the market, featuring sleek design and user-friendly features."
}

# Call the flow with the input dictionary to generate the image prompt
response = client.flow.test(flow, input_dict)

# Output the response (image prompt or generated result)
print(response)
