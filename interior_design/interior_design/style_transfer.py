import os
import replicate
import urllib.request
from decouple import config

def initialize_environment():
    print("Initializing environment variables...")
    # Load the API token from the environment or .env file
    REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN", default=None)
    if not REPLICATE_API_TOKEN:
        raise ValueError("Error: REPLICATE_API_TOKEN is not set in the environment or .env file.")
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    print("Environment initialized successfully.")
    
def validate_image_path(image_path):
    print(f"Validating image path: {image_path}")
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return False
    print("Image file found. Proceeding...")
    return True

def get_replicate_model():
    print("Loading the Replicate model...")
    try:
        model = replicate.models.get("adirik/interior-design")
        version = model.versions.get("76604baddc85b1b4616e1c6475eca080da339c8875bd4996705440484a6eac38")
        print("Model loaded successfully.")
        return version
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def download_image(image_url, output_file_name):
    print(f"Downloading image from URL: {image_url}")
    try:
        urllib.request.urlretrieve(image_url, output_file_name)
        print(f"Image successfully saved to: {output_file_name}")
    except Exception as e:
        print(f"Error downloading image: {str(e)}")

def transfer_style(prompt_text, image_path, output_file_name):
    print("Starting the style transfer process...")
    initialize_environment()
    if not validate_image_path(image_path):
        return

    model_version = get_replicate_model()
    if not model_version:
        print("Style transfer process terminated due to model loading error.")
        return

    try:
        with open(image_path, "rb") as image_file:
            print("Preparing input for prediction...")

            print("Creating prediction...")
            print(prompt_text)
            prediction = replicate.predictions.create(
                version=model_version,
                input={
                    "image": image_file,
                    "prompt": prompt_text,
                    "output_format": "png",
                    "output_quality": 80,
                    "negative_prompt": "blurry, illustration, distorted, horror",
                }
            )

            print("Prediction request submitted. Waiting for the result...")
            while prediction.status in ["starting", "processing"]:
                print(f"Prediction status: {prediction.status}. Please wait...")
                prediction.reload()

            if prediction.status == "succeeded":
                print("Prediction succeeded! Processing the output...")
                
                if isinstance(prediction.output, list) and prediction.output:
                    image_url = prediction.output[0]
                elif isinstance(prediction.output, str):
                    image_url = prediction.output
                else:
                    print("Error: Invalid prediction output format.")
                    return

                download_image(image_url, output_file_name)
            else:
                print(f"Prediction failed. Status: {prediction.status}")
                print(f"Error details: {prediction.error if prediction.error else 'No additional details available'}")

    except Exception as e:
        print(f"An unexpected error occurred during the style transfer process: {str(e)}")

