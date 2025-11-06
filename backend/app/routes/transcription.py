from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.transcription_service import TranscriptionService

router = APIRouter()
transcription_service = TranscriptionService()

@router.post("")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Accepts an audio file and returns transcribed text.
    Currently uses a mock implementation, can be replaced with Whisper.
    """
    try:
        # Validate file type
        if not audio_file.content_type or not audio_file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an audio file."
            )
        
        # Read audio file
        audio_bytes = await audio_file.read()
        
        # Transcribe using service
        transcription_result = await transcription_service.transcribe(audio_bytes, audio_file.filename)
        
        response_data = {
            "success": True,
            "text": transcription_result["text"],
            "confidence": transcription_result.get("confidence", 0.0)
        }
        
        # Include original text if tajweed was applied
        if "original_text" in transcription_result:
            response_data["original_text"] = transcription_result["original_text"]
        
        return JSONResponse(content=response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error transcribing audio: {str(e)}"
        )

