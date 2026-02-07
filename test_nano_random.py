import os
import sys
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    print("Error: GEMINI_API_KEY or GOOGLE_API_KEY not set")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

def generate_random_test():
    """Generate a random test image with Nano Banana Pro."""
    # Using theplural 'generate_images' as revealed by inspection
    prompt = "A futuristic, high-tech HUD interface showing planetary data, neon blue and violet glow, cyberpunk aesthetic, detailed infographics, 4k resolution, sleek design"
    output_path = "web/public/nano_banana_test.png"
    
    print(f"Calling Nano Banana Pro with prompt: {prompt}")
    try:
        response = client.models.generate_images(
            model="nano-banana-pro-preview",
            prompt=prompt,
            config=types.GenerateImageConfig(
                number_of_images=1,
                include_rai_reason=True,
                output_mime_type="image/png"
            )
        )
        
        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            with open(output_path, 'wb') as f:
                f.write(image_data)
            print(f"✓ Success! Image saved to: {output_path}")
            print(f"View it at: http://localhost:3000/nano_banana_test.png")
        else:
            print("✗ No image generated.")
            
    except Exception as e:
        print(f"✗ API Error: {e}")

if __name__ == "__main__":
    generate_random_test()
