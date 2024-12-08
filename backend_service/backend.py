from fastapi import FastAPI, HTTPException, Body, UploadFile, File
import os
import aiofiles
import requests
from fastapi.middleware.cors import CORSMiddleware
from . import s3_service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "files")  # Директория для сохранения файлов

# Убедимся, что директория существует
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# Разрешить CORS-запросы от всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/search")
async def search_endpoint(body: dict = Body(...)):
    """
    Эндпоинт для перенаправления поиска на другой сервис.
    """
    text = body.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")
    try:
        # Перенаправление запроса
        response = requests.post(
            #"http://127.0.0.1:8001/search",
            "http://vllm_fastapi_service:8001/search",
            json={"text": text},
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        for item in data:
            item["src"] = s3_service.convert_path_to_link(item["src"])
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting search service: {str(e)}")
    
@app.post("/semanticsearch")
async def semantic_search_endpoint(body: dict = Body(...)):
    """
    Эндпоинт для перенаправления семантического поиска на другой сервис.
    """
    text = body.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")
    try:
        # Перенаправление запроса
        response = requests.post(
            #"http://127.0.0.1:8001/search",
            "http://vllm_fastapi_service:8001/semanticsearch",
            json={"text": text},
        )
        response.raise_for_status()
        data = response.json()
        data = s3_service.convert(data)
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting search service: {str(e)}")
    
@app.get("/indexing")
async def indexing_endpoint():
    """Эндпоинт для перезагрузки VLLMService."""
    try:
        # Перенаправление запроса
        response = requests.get(
            "http://vllm_fastapi_service:8001/indexing",
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting vllm service: {str(e)}")


@app.post("/upload")
async def upload_endpoint(files: list[UploadFile] = File(...)):
    """
    Эндпоинт для загрузки файлов в папку.
    """
    saved_files = []
    for file in files:
        try:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
            saved_files.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file {file.filename}: {str(e)}")
    return {"message": "Files uploaded successfully", "files": saved_files}
