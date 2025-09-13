# routers/images.py

import os
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from PIL import Image
import io

from auth_utils import get_current_active_user
import schemas
from pydantic import BaseModel

try:
    from ai_image_service import ai_image_service
    AI_IMAGE_SERVICE_AVAILABLE = True
except ImportError:
    AI_IMAGE_SERVICE_AVAILABLE = False
    ai_image_service = None

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

# Configure Cloudinary using environment variables from your .env file
# Make sure you have added these to your .env file
cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

@router.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Uploads an image file to Cloudinary after pre-processing.
    - Requires authentication.
    - Resizes image to a max of 1920x1080.
    - Converts image to WEBP format for efficiency.
    - Returns the secure URL and public ID for the uploaded image.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read image contents into memory
        contents = await file.read()
        
        # Open with Pillow
        img = Image.open(io.BytesIO(contents))
        
        # Resize the image to a maximum dimension (e.g., 1920x1080) while maintaining aspect ratio
        img.thumbnail((1920, 1080))
        
        # Save the processed image to a byte stream in WEBP format
        processed_image_io = io.BytesIO()
        img.save(processed_image_io, format='WEBP', quality=85)
        processed_image_io.seek(0)

        # Upload the processed image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            processed_image_io,
            folder="image_gallery_posts" # Organizes uploads in a specific folder
        )
        
        return {
            "message": "Image uploaded successfully!",
            "url": upload_result.get("secure_url"),
            "public_id": upload_result.get("public_id")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error uploading the file: {e}"
        )

class ImageGenerationRequest(BaseModel):
    prompt: str

@router.post("/generate/")
async def generate_ai_image(
    request: ImageGenerationRequest,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Generates an AI image using Hugging Face's Stable Diffusion API.
    - Requires authentication.
    - Takes a text prompt and generates an image.
    - Uploads the generated image to Cloudinary.
    - Returns the secure URL and public ID for the generated image.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    if not AI_IMAGE_SERVICE_AVAILABLE or not ai_image_service:
        raise HTTPException(
            status_code=503,
            detail="AI image generation not available. Please install required dependencies: pip install requests"
        )
    
    try:
        # Generate image using AI service
        result = await ai_image_service.generate_image(request.prompt)
        
        return {
            "message": "AI image generated successfully!",
            "url": result["image_url"],
            "public_id": result["image_public_id"],
            "prompt": request.prompt
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error generating the image: {e}"
        )