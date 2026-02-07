import os
import sys
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent / 'execution'))
import database

load_dotenv()

def test_single_generation():
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    
    # 1. Get one distilled article
    database.init_db()
    pending = database.get_articles_by_status('distilled', limit=1)
    if not pending:
        print("No distilled articles found.")
        return
    
    post = pending[0]
    print(f"Testing generation for: {post['title']}")
    
    # 2. Setup paths
    output_dir = Path('web/public/feed')
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"DEBUG_TEST_{post['id'][:8]}.png"
    output_path = output_dir / filename
    
    # 3. Create prompt
    from generate_ai_visuals import create_visual_prompt
    prompt = create_visual_prompt(post)
    print(f"Prompt: {prompt[:100]}...")
    
    # 4. Generate
    model_id = "gemini-3-pro-image-preview"
    print(f"Calling {model_id}...")
    try:
        response = client.models.generate_images(
            model=model_id,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/png"
            )
        )
        
        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            with open(output_path, 'wb') as f:
                f.write(image_data)
            print(f"✓ SUCCESS: Saved to {output_path}")
        else:
            print("✗ ERROR: No images in response")
            print(f"Full response: {response}")
    except Exception as e:
        print(f"✗ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_single_generation()
