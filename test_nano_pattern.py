import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def test_nano_banana_pattern():
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    model_id = "gemini-3-pro-image-preview"
    prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme. Futuristic HUD style."
    
    print(f"Testing Nano Banana Pro pattern with model: {model_id}")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=[prompt],
        )

        found_image = False
        for i, part in enumerate(response.parts):
            if part.text:
                print(f"Text part: {part.text}")
            elif part.inline_data:
                # In the genai SDK, as_image() is often used if PIL is installed
                # or we can access the bytes directly.
                try:
                    image = part.as_image()
                    image.save("web/public/nano_banana_test_pattern.png")
                    print(f"✓ Success! Image part found and saved to web/public/nano_banana_test_pattern.png")
                    found_image = True
                except Exception as e:
                    print(f"Error saving image part: {e}")
                    # Fallback to direct bytes if as_image() fails
                    if hasattr(part.inline_data, 'data'):
                        with open("web/public/nano_banana_test_pattern.png", "wb") as f:
                            f.write(part.inline_data.data)
                        print(f"✓ Success! Image part found and saved via raw bytes.")
                        found_image = True
        
        if not found_image:
            print("✗ No image part found in response.")
            print(f"Response parts: {[type(p) for p in response.parts]}")

    except Exception as e:
        print(f"✗ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_nano_banana_pattern()
