"""Image upload API with WebP conversion."""

from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from PIL import Image
import io
from app.dependencies import require_admin
from app.models.user import User

router = APIRouter(prefix="/api/admin/upload", tags=["admin-upload"])

# Upload directory
UPLOAD_DIR = Path(__file__).parent.parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed image types
ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin)
):
    """
    Upload image and convert to WebP format.
    
    Args:
        file: Uploaded image file
        current_user: Current admin user
        
    Returns:
        Image URL
        
    Raises:
        HTTPException: If file is invalid or upload fails
    """
    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_TYPES)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    try:
        # Open image with Pillow
        image = Image.open(io.BytesIO(content))
        
        # Convert to RGB if necessary (for transparency handling)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"{timestamp}.webp"
        filepath = UPLOAD_DIR / filename
        
        # Save as WebP with optimization
        image.save(
            filepath,
            'WEBP',
            quality=85,
            method=6,  # Best compression
            optimize=True
        )
        
        # Return URL
        url = f"/static/uploads/{filename}"
        
        return {
            "success": True,
            "url": url,
            "filename": filename,
            "size": filepath.stat().st_size
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process image: {str(e)}"
        )


@router.delete("/image")
async def delete_image(
    filename: str,
    current_user: User = Depends(require_admin)
):
    """
    Delete an uploaded image.
    
    Args:
        filename: Name of the file to delete
        current_user: Current admin user
        
    Returns:
        Success message
    """
    filepath = UPLOAD_DIR / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        filepath.unlink()
        return {"success": True, "message": "Image deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete image: {str(e)}"
        )

