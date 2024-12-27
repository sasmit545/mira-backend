import base64
import os
import requests
import urllib.parse
import traceback
import cloudinary
import cloudinary.uploader
from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is not set. Please check your .env file.")

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Initialize the MiraClient
client = MiraClient(config={"API_KEY": api_key})

# Define the image generation API endpoint
IMAGE_API_URL = "https://image.pollinations.ai/prompt/{prompt}"

# Helper function to upload images to Cloudinary
def upload_to_cloudinary(image_path):
    try:
        # Upload the image file to Cloudinary
        response = cloudinary.uploader.upload(
            file=image_path,
            resource_type="image"  # Specify it's an image
        )
        return response["secure_url"]  # Return the secure URL of the hosted image
    except Exception as e:
        print(f"Error uploading to Cloudinary: {str(e)}")
        traceback.print_exc()
        return None

# Helper function to call the image generation API
def generate_image(prompt, model=None, seed=None, width=1024, height=1024, nologo=True, private=False, enhance=False, safe=True):
    try:
        # URL-encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Build the query string
        params = {
            "model": model,
            "seed": seed,
            "width": width,
            "height": height,
            "nologo": str(nologo).lower(),
            "private": str(private).lower(),
            "enhance": str(enhance).lower(),
            "safe": str(safe).lower()
        }
        query_string = "&".join(f"{key}={urllib.parse.quote(str(value))}" for key, value in params.items() if value is not None)
        
        # Send the GET request to fetch the image
        response = requests.get(f"{IMAGE_API_URL.replace('{prompt}', encoded_prompt)}?{query_string}", stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the image to a temporary file
        temp_image_path = "generated_image.jpg"
        with open(temp_image_path, "wb") as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                image_file.write(chunk)
        
        # Upload the image to Cloudinary
        cloudinary_url = upload_to_cloudinary(temp_image_path)
        
        # Clean up the temporary file
        os.remove(temp_image_path)
        
        return cloudinary_url if cloudinary_url else "Error hosting image on Cloudinary."

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        traceback.print_exc()
        return None

# Define flows and their test inputs
test_flows = [
    {
        "name": "Hero Image Generator",
        "file": "flow-hero.yaml",
        "inputs": {
            "brandName": "TechCorp",
            "campaignTheme": "Summer Tech Festival",
            "moodKeywords": ["vibrant", "modern", "energetic"],
            "targetAudience": "Tech-savvy millennials"
        }
    },
    {
        "name": "Product Showcase Generator",
        "file": "flow-prod.yaml",
        "inputs": {
            "productName": "UltraPhone X",
            "productFeatures": ["edge-to-edge display", "dual camera", "wireless charging"],
            "environment": "Modern minimalist workspace",
            "style": "Clean and professional with soft lighting"
        }
    },
    {
        "name": "Promotional Banner Generator",
        "file": "flow-banner.yaml",
        "inputs": {
            "offerType": "Flash Sale",
            "discountDetails": "50% OFF",
            "targetAudience": "Budget-conscious shoppers",
            "bannerSize": "728x90"
        }
    }
]

# Test each flow and generate images
for flow_config in test_flows:
    try:
        print(f"\n{'='*50}")
        print(f"Testing {flow_config['name']}...\n{'='*50}")
        
        # Load the flow
        flow = Flow(source=flow_config['file'])
        
        # Test the flow with inputs
        response = client.flow.test(flow, flow_config['inputs'])
        
        # Extract prompt from inputs for image generation
        prompt = response['result']  # Example: Use inputs as a text description
        
        # Generate an image for the flow
        image_url = generate_image(prompt)
        
        # Print formatted response and image URL
        print(f"\nResponse for {flow_config['name']}:")
        print(json.dumps(response, indent=2))
        print(f"Generated Image URL: {image_url}")
        print(f"✓ {flow_config['name']} tested successfully!")
        
    except Exception as e:
        print(f"✗ Error testing {flow_config['name']}: {str(e)}")
        traceback.print_exc()
