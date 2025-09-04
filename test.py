import requests
import io
import json

# Replace with your API's URL if it's different
BASE_URL = "http://127.0.0.1:8000"

def create_dummy_image(filename="test_logo.png"):
    """
    Creates a simple dummy PNG image in memory for testing.
    """
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (100, 100), color = 'red')
    d = ImageDraw.Draw(img)
    d.text((10,10), "Logo", fill=(255,255,255))
    
    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format='PNG')
    img_bytes_io.seek(0)
    return img_bytes_io, filename

def test_generate_brand_asset_endpoint():
    """
    Tests the POST / endpoint by sending a dummy image and form data.
    """
    url = f"{BASE_URL}/"
    
    # Create the in-memory dummy image file
    image_file, filename = create_dummy_image()
    
    # Define the form data fields
    data = {
        'logo_description': 'A simple red circle logo with the word "Logo" in white.',
        'brand_palette': '#FF0000, #FFFFFF, #000000',
        'visual_use_case': 'Social media ad',
        'style': 'minimalist'
    }

    # Define the file to be sent
    files = {
        'logo_photo': (filename, image_file, 'image/png')
    }

    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status() # Raises an HTTPError if the status is 4xx or 5xx

        print("\nRequest successful!")
        print("Status Code:", response.status_code)
        
        # Pretty print the JSON response
        try:
            response_json = response.json()
            print("Response Body (JSON):")
            print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            print("Raw Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    test_generate_brand_asset_endpoint()