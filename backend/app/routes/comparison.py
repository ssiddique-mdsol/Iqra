from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.comparison_service import ComparisonService

router = APIRouter()
comparison_service = ComparisonService()

class ComparisonRequest(BaseModel):
    recognized_text: str
    verse_text: str
    verse_reference: str = ""  # Optional: e.g., "2:255"

@router.post("")
async def compare_verse(request: ComparisonRequest):
    """
    Compares recognized text to a given Qur'an verse and returns match/mismatch data.
    """
    try:
        if not request.recognized_text or not request.verse_text:
            raise HTTPException(
                status_code=400,
                detail="Both recognized_text and verse_text are required"
            )
        
        comparison_result = comparison_service.compare(
            recognized_text=request.recognized_text,
            verse_text=request.verse_text
        )
        
        return {
            "success": True,
            "match_percentage": comparison_result["match_percentage"],
            "word_comparisons": comparison_result["word_comparisons"],
            "total_words": comparison_result["total_words"],
            "matched_words": comparison_result["matched_words"],
            "mismatched_words": comparison_result["mismatched_words"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing texts: {str(e)}"
        )

