from fastapi import FastAPI, HTTPException, Body
from vllm import VLLMService
import os
import platform
from fastapi.middleware.cors import CORSMiddleware
from llama import LlamaModel

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
# vllm_api = VLLMFastAPI()
# llama = LlamaModel()

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
    vllm_api = VLLMFastAPI()
    llama = LlamaModel()
    text = body.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")
    try:
        results = vllm_api.vllm_service.search(text)

        # Проверяем, есть ли метаданные с file_path
        file_path = results[0].metadata[0]['file_path']
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="Invalid or missing file path in metadata.")
        
        # Объединяем содержимое всех PDF с указанием названий файлов
        combined_content = ""
        for file in results:
            try:
                pdf_file = file.metadata[0]['file_path']
                pdf_text = llama.extract_text_from_pdf(pdf_file)
                combined_content += f"\nFrom file '{pdf_file}':\n{pdf_text}\n"
            except Exception as e:
                print(f"Ошибка обработки файла {pdf_file}: {str(e)}")
        
        # Генерируем текст с помощью Llama
        llama_response = llama.generate_text(text, combined_content)
        summary = llama.summary(llama_response)

        # Добавляем llama_response в метаданные
        results[0]["metadata"][0]["llama_response"] = summary

        return {"result": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# return {
#             content: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " +
#                 "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an " +
#                 "unknown printer took a galley of type and scrambled it to make a type specimen book." +
#                 " It has survived not only five centuries, but also the leap into electronic typesetting, " +
#                 "remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset" +
#                 " sheets containing Lorem Ipsum passages, and more recently with desktop publishing software " +
#                 "like Aldus PageMaker including versions of Lorem Ipsum.\n",
#             sources: [
#                 {title: "Source1", pages: [12, 13], src: "https://google.com"},
#                 {title: "Source2", pages: [1], src: "https://google.com"},
#                 {title: "Source3", pages: [2, 3], src: "https://google.com"},
#             ],
#         }

@app.get("/indexing")
async def indexing_endpoint():
    """Эндпоинт для перезагрузки VLLMService."""
    try:
        vllm_api.reload_service()
        return {"message": "Indexing reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "vllm_fastapi:app",  # main - имя файла, app - объект приложения FastAPI
        host="0.0.0.0",  # Слушать на всех интерфейсах
        port=8000,       # Указать порт
        reload=False      # Перезагрузка при изменениях (для разработки)
    )