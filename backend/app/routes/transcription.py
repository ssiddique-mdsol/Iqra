from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.services.transcription_service import TranscriptionService

# Ensure .env is loaded
load_dotenv()

router = APIRouter()

# Lazy initialization - create service on first use to ensure .env is loaded
_transcription_service = None

def get_transcription_service():
    """Get transcription service instance, creating it if needed."""
    global _transcription_service
    if _transcription_service is None:
        # Ensure .env is loaded before creating service
        load_dotenv()
        _transcription_service = TranscriptionService()
        print(f"[Route] TranscriptionService created: use_whisper={_transcription_service.use_whisper}, model={_transcription_service.model is not None}")
    return _transcription_service

@router.post("")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Accepts an audio file and returns transcribed text.
    Currently uses a mock implementation, can be replaced with Whisper.
    """
    try:
        print(f"[API] ========================================")
        print(f"[API] Received transcription request")
        print(f"[API] Audio file: {audio_file.filename}")
        print(f"[API] Content type: {audio_file.content_type}")
        
        # Validate file type (be more lenient for mobile uploads)
        if audio_file.content_type and not audio_file.content_type.startswith("audio/"):
            print(f"[API] Warning: Unexpected content type: {audio_file.content_type}")
            # Don't reject, just warn - mobile might send different types
        
        # Read audio file
        audio_bytes = await audio_file.read()
        print(f"[API] Audio file size: {len(audio_bytes)} bytes")
        print(f"[API] Audio file type: {audio_file.content_type}")
        print(f"[API] Audio filename: {audio_file.filename}")
        
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty. Please record again."
            )
        
        # Check if audio file has valid header (basic validation)
        if len(audio_bytes) < 100:
            raise HTTPException(
                status_code=400,
                detail=f"Audio file too small ({len(audio_bytes)} bytes). Please record again."
            )
        
        # Log first few bytes to check format
        print(f"[API] First 20 bytes (hex): {audio_bytes[:20].hex()}")
        
        # Transcribe using service (lazy initialization)
        print(f"[API] Calling transcription service...")
        transcription_service = get_transcription_service()
        transcription_result = await transcription_service.transcribe(audio_bytes, audio_file.filename)
        print(f"[API] Transcription completed: {transcription_result.get('text', '')[:50]}...")
        
        response_data = {
            "success": True,
            "text": transcription_result["text"],
            "confidence": transcription_result.get("confidence", 0.0)
        }
        
        # Include original text if tajweed was applied
        if "original_text" in transcription_result:
            response_data["original_text"] = transcription_result["original_text"]
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"[API] ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error transcribing audio: {str(e)}"
        )

