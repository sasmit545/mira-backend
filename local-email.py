from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

# Load the flow YAML (Email Content Generation)


# Prepare the input dictionary with email campaign details
input_dict = {
    "productName": "SuperWidget",
    "productDescription": "The most advanced widget on the market, featuring sleek design and user-friendly features.",
    "productOffer": "50% off for a limited time!",
    "companyName": "AwesomeTech",
    "productLink": "https://example.com/superwidget",
    "companyLogo": "https://example.com/logo.png",
    "ctaText": "Shop Now"
}

# Call the flow with the input dictionary to generate the email content
response = client.flow.execute("sasmit/email-content-generation", input_dict)

# Output the response (email content)
print(response['result'])
