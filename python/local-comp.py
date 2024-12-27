from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the client with hardcoded API key
# Note: Replace with your actual API key or use environment variable
api_key = os.getenv("API_KEY")
client = MiraClient(config={"API_KEY": api_key})

# Load the compound flow YAML
flow = Flow(source="flow-cop-img.yaml")

# Hardcoded input dictionary with all required fields
input_dict = {
    "productName": "UltraPhone X",
    "productDescription": "Next-generation smartphone with AI capabilities and edge-to-edge display",
    "productOffer": "Holiday Special: 30% OFF",
    "companyName": "TechCorp",
    "productLink": "https://techcorp.com/ultraphone-x",
    "companyLogo": "https://techcorp.com/logo.png",
    "ctaText": "Shop Now"
}

# Call the flow with the input dictionary
response = client.flow.test(flow, input_dict)

# Print the response
print(response)