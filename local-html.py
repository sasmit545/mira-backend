from mira_sdk.exceptions import FlowError
from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os

# Initialize Mira Client with API Key
# Load environment variables from .env file
load_dotenv()

# Initialize the client with hardcoded API key
# Note: Replace with your actual API key or use environment variable
api_key = os.getenv("API_KEY")
client = MiraClient(config={"API_KEY": api_key})

# Load your flow configuration from the YAML file
flow = Flow("sasmit/email-html-generator")  # Update the path

# Prepare test inputs
test_input = {
    "hero_img_url": "https://res.cloudinary.com/dfgoyoeml/image/upload/v1735223455/eowtjmgshrxaor1kx5gr.jpg",  # URL for the hero section image
    "product_img_url": "https://res.cloudinary.com/dfgoyoeml/image/upload/v1735223480/okw5rhs2i44yyk0z88a2.jpg",  # URL for the product image
    "banner_img_url": "https://res.cloudinary.com/dfgoyoeml/image/upload/v1735223538/urvqexzcpikzxdnlzngd.jpg",  # URL for the banner image
    "email_content": "Here is a product showcase image prompt that highlights the UltraPhone X:\n\n**Image Prompt:**\n\nCreate a visually stunning product showcase image featuring the UltraPhone X in a modern minimalist workspace. The scene should be set against a clean and sleek desk with a subtle wooden texture, complemented by a soft gray or white background.\n\n**Product Placement:**\n\nPosition the UltraPhone X as the central focus of the image, placed on the desk at a 45-degree angle to create depth and dimension. The phone should be displayed in a way that showcases its striking edge-to-edge display, with the screen illuminated to highlight its vibrant colors and crystal-clear resolution.\n\n**Key Feature Highlights:**\n\n1. **Dual Camera:** Emphasize the dual camera setup by positioning the phone in a way that the camera module is clearly visible. Use soft lighting to create a subtle shadow effect, highlighting the camera's sleek design and advanced features.\n2. **Wireless Charging:** Place a wireless charging pad next to the phone, with the charging indicator lights softly glowing to demonstrate the convenience and innovation of this feature.",  # Content for the email
    "product_url": "https://example.com/product"  # URL for the product page
}

# Testing the flow with the prepared inputs
try:
    response = client.flow.execute("sasmit/email-html-generator", test_input)  # Test entire pipeline
    print("Test response:", response['result'])  # Print the response
except FlowError as e:
    print("Test failed:", str(e))  # Handle test failure
