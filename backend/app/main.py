from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcription, comparison

app = FastAPI(
    title="Iqra API",
    description="AI Speech-to-Text + Qur'an text comparison service",
    version="1.0.0"
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

@app.get("/")
async def root():
    return {"message": "Iqra API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

