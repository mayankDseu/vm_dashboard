from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from streams.stream_handler import VideoStreamHandler

import os

app = FastAPI(title="VMS Test API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="outputs"), name="static")

#  Health check endpoint
@app.get("/ping")
async def ping():
    return {"message": "API is alive"}


stream_handlers = {}


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_VIDEO_PATHS = [os.path.join(PROJECT_ROOT, "inputs", "sample_videos", f"video{i}.mp4") for i in range(1, 11)]

# ▶️ Start streams
@app.post("/start-streams")
async def start_streams(background_tasks: BackgroundTasks):
    for i, path in enumerate(SAMPLE_VIDEO_PATHS):
        handler = VideoStreamHandler(i, path)
        handler.start()
        stream_handlers[i] = handler
    return {"status": "Streams started"}

# Get results (detections + classification)
@app.get("/get-results")
async def get_results():
    return {
        stream_id: handler.predictions
        for stream_id, handler in stream_handlers.items()
        if handler.running
    }
