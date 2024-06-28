from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import glob
import shutil
from downloader import Downloader
from demucs_processor import DemucsProcessor
from spotify_to_yt import ConvertSpofity

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

global filename
demucs_processor = DemucsProcessor()
downloader = Downloader()


class DownloadRequest(BaseModel):
    url: str
    filetype: str


class ProcessRequest(BaseModel):
    filename: str
    filetype: str
    numStems: int


@app.get("/")
async def home(request: Request):
    refresh_directories()
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/delete")
async def delete(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download_video")
async def download_audio(request: DownloadRequest):
    input_url = request.url
    if "spotify" in input_url:
        url = ConvertSpofity(input_url).get_youtube_url()
    else:
        url = input_url

    if url:
        filename = downloader.download_video(url, request.filetype)
        print("filename", filename)
        return {"status": "success", "filename": str(filename)}


@app.post("/process_audio")
async def process_audio(request: ProcessRequest):
    demucs_processor.process_audio(request.filename, request.filetype, request.numStems)
    return {"message": "Finished", "filename": str(request.filename)}


@app.get("/download")
async def download(filename: str):
    file_path = f"{filename}.zip"
    if os.path.exists(file_path):
        response = FileResponse(file_path, filename=os.path.basename(file_path))
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/tracks/{stem_type}/{songname}")
async def serve_audio(stem_type: str, songname: str):
    directory = f"tracks/{stem_type}/{songname}"
    if os.path.exists(directory):
        files = os.listdir(directory)
        return JSONResponse(content=files)
    else:
        raise HTTPException(status_code=404, detail="Directory not found")


@app.get("/tracks/{stem_type}/{songname}/{filename}")
async def serve_file(stem_type: str, songname: str, filename: str):
    file_path = f"tracks/{stem_type}/{songname}/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


def refresh_directories():
    for directory in glob.glob("tracks/htdemucs/*"):
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    for directory in glob.glob("tracks/htdemucs_6s/*"):
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    for file in glob.glob("*.mp3") + glob.glob("*.wav") + glob.glob("*.flac"):
        os.remove(file)


@app.get("/flaskwebgui-keep-server-alive")
async def keep_alive():
    return "Server is alive"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
