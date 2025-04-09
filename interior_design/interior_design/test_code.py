import os
import replicate
import urllib.request
from decouple import config

REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def remodel_image(prompt_text,output_file_name):
    image_path = "test.jpg" 
    print(f"Using image: {image_path}")
    try:
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            return

        print("Loading the model...")
        model = replicate.models.get("adirik/interior-design")
        version = model.versions.get("76604baddc85b1b4616e1c6475eca080da339c8875bd4996705440484a6eac38")

        with open(image_path, "rb") as image_file:

            print("Creating prediction...")
            prediction = replicate.predictions.create(
                version=version,
                input={
                    "image": image_file,
                    "prompt": prompt_text,
                    "output_format": "png",
                    "output_quality": 80,
                    "negative_prompt": "blurry, illustration, distorted, horror",
                }
            )

        print("Processing image... This may take a while.")
        while prediction.status in ["starting", "processing"]:
            prediction.reload()

        if prediction.status == "succeeded":
            print(f"Prediction succeeded. Output: {prediction.output}")
            
            if isinstance(prediction.output, list) and prediction.output:
                image_url = prediction.output[0]
            elif isinstance(prediction.output, str):
                image_url = prediction.output
            else:
                print("Error: Prediction output is not a valid URL or list of URLs.")
                return

            file_name = 'output.png'
            urllib.request.urlretrieve(image_url, output_file_name)
            print(f"Remodeled image saved to: {output_file_name}")
        else:
            print(f"Prediction failed with status: {prediction.status}")
            print(f"Error details: {prediction.error if prediction.error else 'No error details available'}")
        return file_name

    except Exception as e:
        print(f"Error: {str(e)}")


    
