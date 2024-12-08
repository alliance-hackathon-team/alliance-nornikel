from fastapi import FastAPI, HTTPException, Body
from vllm import VLLMService
import os
import platform
from fastapi.middleware.cors import CORSMiddleware
from llama import LlamaModel
import os

HOST_CUT_PDF_PATH = os.getenv("HOST_CUT_PDF_PATH", "/app/cut_pdf")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class VLLMFastAPI:
    """Класс для управления экземпляром VLLMService."""
    
    def __init__(self):
        self.vllm_service = self.initialize_vllm_service()

    def initialize_vllm_service(self):
        """Инициализация VLLMService."""
        return VLLMService(
            model_name="vidore/colpali-v1.3",
            device="mps" if platform.system().lower() == 'darwin' else "cuda",
            folder=os.path.join(BASE_DIR, "files")
        )

    def reload_service(self):
        """Перезагрузка VLLMService."""
        self.vllm_service = self.initialize_vllm_service()

# Создаем экземпляр класса
vllm_api = VLLMFastAPI()
llama = LlamaModel()

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
    """Эндпоинт для поиска по тексту."""
    text = body.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")
    try:
        results = vllm_api.vllm_service.search(text)
        return {"result": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/semanticsearch")
async def semantic_search_endpoint(body: dict = Body(...)):
    """Эндпоинт для семантического поиска по тексту."""
    text = body.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")
    try:
        results = vllm_api.vllm_service.search(text)

        # Проверяем, есть ли метаданные с file_path
        file_path = results[0].metadata[0]['file_path']
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="Invalid or missing file path in metadata.")
        
        sources = []
        linux_dir = []
        for file in results:
            title = file.metadata[0]['title']
            pages = file.page_num

            if '\\' in HOST_CUT_PDF_PATH:
                src_path_cut = f"{HOST_CUT_PDF_PATH}\\{title}\\{title}_{pages}.pdf"
            else:
                src_path_cut = os.path.join(HOST_CUT_PDF_PATH, f"{title}_{pages}.pdf")

            sources.append(dict(
                title=title, 
                pages=pages,
                src=src_path_cut,
            ))

            linux_dir.append(dict(
                title=title, 
                pages=pages,
                src=os.path.join(f"/app/cut_pdf/{title}", f"{title}_{pages}.pdf"),
            ))
        
        # Объединяем содержимое всех PDF с указанием названий файлов
        combined_content = ""
        for file in results:
            try:
                cut_pdf_src = [s for s in linux_dir if s['title'] == file.metadata[0]['title']]
                if cut_pdf_src:
                    cut_pdf_src = cut_pdf_src[0]['src']
                else:
                    cut_pdf_src = file.metadata[0]['file_path']

                pdf_text = llama.extract_text_from_pdf(cut_pdf_src)
                combined_content += f"\nFrom file '{cut_pdf_src}':\n{pdf_text}\n"
            except Exception as e:
                print(f"Ошибка обработки файла {cut_pdf_src}: {str(e)}")
        
        # Генерируем текст с помощью Llama
        llama_response = llama.generate_text(text, combined_content)
        summary = llama.summary(text, llama_response)

        return {"content": summary, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indexing")
async def indexing_endpoint():
    """Эндпоинт для перезагрузки VLLMService."""
    try:
        vllm_api.reload_service()
        return {"message": "Indexing reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))