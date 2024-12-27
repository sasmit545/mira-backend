from flask import Flask, request, jsonify
from flask_cors import CORS
from mira_sdk import MiraClient
from dotenv import load_dotenv
import os
import json
import cloudinary
import cloudinary.uploader
import urllib.parse
import requests

app = Flask(__name__)
CORS(app)

load_dotenv()
api_key = os.getenv("API_KEY")
client = MiraClient(config={"API_KEY": api_key})

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

IMAGE_API_URL = "https://image.pollinations.ai/prompt/{prompt}"

def upload_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(file=image_path, resource_type="image")
        return response["secure_url"]
    except Exception as e:
        return {"error": str(e)}, 500

def generate_image(prompt, width, height, model=None, seed=None):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        params = {
            "model": model, "seed": seed, "width": width, "height": height,
            "nologo": "true", "safe": "true"
        }
        query_string = "&".join(f"{key}={urllib.parse.quote(str(value))}" 
                              for key, value in params.items() if value is not None)
        
        response = requests.get(f"{IMAGE_API_URL.replace('{prompt}', encoded_prompt)}?{query_string}", 
                              stream=True)
        response.raise_for_status()

        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                image_file.write(chunk)
        
        cloudinary_url = upload_to_cloudinary(temp_image_path)
        os.remove(temp_image_path)
        return cloudinary_url
    except Exception as e:
        return {"error": str(e)}, 500

def validate_input(data):
    required_fields = ["productName", "productDescription", "productOffer", 
                      "companyName", "productLink", "companyLogo", "ctaText", 
                      "campaignTheme"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return True

@app.route("/api/generate-email", methods=["POST"])
def generate_email():
    try:
        data = request.json
        validate_input(data)
        
        test_flows = [
            {
                "name": "Hero Image Generator",
                "path": "sasmit/email-hero-image-generator",
                "inputs": {
                    "brandName": data["companyName"],
                    "campaignTheme": data["campaignTheme"],
                    "moodKeywords": ["vibrant", "modern", "energetic"],
                    "targetAudience": "millennials"
                },
                "width": 600,
                "height": 300
            },
            {
                "name": "Product Showcase Generator",
                "path": "sasmit/email-product-showcase-generator",
                "inputs": {
                    "productName": data["productName"],
                    "productFeatures": [data["productDescription"]],
                    "environment": "Modern minimalistic ",
                    "style": "Clean and professional with soft lighting"
                },
                "width": 300,
                "height": 300
            },
            {
                "name": "Promotional Banner Generator",
                "path": "sasmit/email-promo-banner-generator",
                "inputs": {
                    "offerType": "Flash Sale",
                    "discountDetails": data["productOffer"],
                    "targetAudience": "Budget-conscious shoppers",
                    "bannerSize": "728x90"
                },
                "width": 600,
                "height": 200
            }
        ]

        generated_images = {}
        for flow in test_flows:
            response = client.flow.execute(flow["path"], flow["inputs"])
            prompt = response['result']
            image_url = generate_image(prompt, flow["width"], flow["height"])
            generated_images[flow["name"]] = image_url

        email_content = client.flow.execute("sasmit/email-content-generation", data)

        html_input = {
            "hero_img_url": generated_images["Hero Image Generator"],
            "product_img_url": generated_images["Product Showcase Generator"],
            "banner_img_url": generated_images["Promotional Banner Generator"],
            "email_content": email_content["result"],
            "product_url": data["productLink"]
        }
        html_response = client.flow.execute("sasmit/email-html-generator", html_input)

        return jsonify({
            "html": html_response["result"]
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(debug=False, host="0.0.0.0", port=port)
