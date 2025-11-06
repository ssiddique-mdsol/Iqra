from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.tajweed_service import TajweedService

router = APIRouter()
tajweed_service = TajweedService()

class TajweedRequest(BaseModel):
    text: str

@router.post("")
async def add_tajweed(request: TajweedRequest):
    """
    Add tajweed (diacritics) to Arabic text.
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text is required"
            )
        
        text_with_tajweed = tajweed_service.add_tajweed(request.text)
        
        return {
            "success": True,
            "text_with_tajweed": text_with_tajweed,
            "original_text": request.text
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error adding tajweed: {str(e)}"
        )

