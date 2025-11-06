from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load .env file FIRST before importing routes
load_dotenv()

from app.routes import transcription, comparison, tajweed

app = FastAPI(
    title="Iqra API",
    description="AI Speech-to-Text + Qur'an text comparison service",
    version="1.0.0"
)

# Add exception handler for validation errors to see what's wrong
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    print(f"[API] ========================================")
    print(f"[API] Validation Error (422):")
    print(f"[API] Errors: {exc.errors()}")
    print(f"[API] Request method: {request.method}")
    print(f"[API] Request URL: {request.url}")
    print(f"[API] Request headers: {dict(request.headers)}")
    print(f"[API] Request body (first 500 bytes): {body[:500]}")
    print(f"[API] ========================================")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "message": "Validation error - check backend logs for details"}
    )

# CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcription.router, prefix="/transcribe_audio", tags=["transcription"])
app.include_router(comparison.router, prefix="/compare_verse", tags=["comparison"])
app.include_router(tajweed.router, prefix="/add_tajweed", tags=["tajweed"])

@app.get("/")
async def root():
    return {"message": "Iqra API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test-whisper")
async def test_whisper():
    """Test endpoint to check if Whisper is loaded."""
    from app.routes.transcription import get_transcription_service
    service = get_transcription_service()
    return {
        "use_whisper": service.use_whisper,
        "model_loaded": service.model is not None,
        "whisper_available": hasattr(service, 'model') and service.model is not None,
        "status": "Whisper is loaded and ready!" if (service.use_whisper and service.model is not None) else "Using mock (Whisper not available)"
    }

@app.get("/debug-transcription")
async def debug_transcription():
    """Debug endpoint to test transcription with dummy data."""
    from app.routes.transcription import get_transcription_service
    import asyncio
    
    service = get_transcription_service()
    
    # Create dummy audio bytes
    dummy_audio = b"fake audio data for testing" * 100
    
    # Test transcription
    result = await service.transcribe(dummy_audio, "test.m4a")
    
    return {
        "service_use_whisper": service.use_whisper,
        "service_model_loaded": service.model is not None,
        "transcription_confidence": result.get("confidence"),
        "transcription_text": result.get("text", "")[:100],
        "is_mock": result.get("confidence") == 0.85,
        "status": "Using MOCK" if result.get("confidence") == 0.85 else "Using Whisper"
    }

