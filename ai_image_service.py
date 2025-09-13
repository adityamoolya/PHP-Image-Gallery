# ai_image_service.py

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests library not installed. Install with: pip install requests")

import cloudinary.uploader
import logging

try:
    from config import HUGGINGFACE_API_KEY, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
except ImportError:
    HUGGINGFACE_API_KEY = None
    CLOUDINARY_CLOUD_NAME = None
    CLOUDINARY_API_KEY = None
    CLOUDINARY_API_SECRET = None

logger = logging.getLogger(__name__)

class AIImageService:
    def __init__(self):
        self.hf_api_key = HUGGINGFACE_API_KEY
        self.model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET
        )
    
    async def generate_image(self, prompt: str) -> dict:
        """
        Generate an image using Hugging Face's Stable Diffusion API
        Returns a dictionary with image_url and image_public_id
        """
        if not REQUESTS_AVAILABLE:
            raise ValueError("requests library not available. Install with: pip install requests")
        
        if not self.hf_api_key:
            raise ValueError("Hugging Face API key not configured")
        
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        
        # Prepare the request payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
        
        try:
            # Make request to Hugging Face API
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Get the image data
            image_data = response.content
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                image_data,
                folder="ai-generated",
                resource_type="image",
                format="jpg"
            )
            
            return {
                "image_url": upload_result["secure_url"],
                "image_public_id": upload_result["public_id"]
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Hugging Face API request failed: {e}")
            raise Exception(f"Failed to generate image: {str(e)}")
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            raise Exception(f"Failed to process generated image: {str(e)}")

# Global instance
ai_image_service = AIImageService()
