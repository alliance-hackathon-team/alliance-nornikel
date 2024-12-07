from byaldi import RAGMultiModalModel
import os
from datetime import datetime

class VLLMService:
    def __init__(self, model_name="vidore/colpali-v1.3", device="mps", folder="files"):
        self.device = device
        self.model_name = model_name
        self.folder = folder
        self.index_name = "image_index"
        self.RAG = None
        self.indexed = False

        self._initialize_model()

    def _initialize_model(self):
        # Загружаем модель
        self.RAG = RAGMultiModalModel.from_pretrained(self.model_name, device=self.device)
        # Индексируем файлы в папке
        metadatas = []
        metadatas.extend([self.get_file_metadata(f) for f in self._get_files_from_folder(self.folder)])
        self.RAG.index(
            input_path=self.folder,
            index_name=self.index_name,
            store_collection_with_index=False,
            metadata=metadatas,
            overwrite=True
        )
        self.indexed = True

    def search(self, text, k=5):
        # Выполняем поиск
        results = self.RAG.search(text, k=k)
        return results

    def get_file_metadata(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        
        # Получаем название файла без расширения и расширение
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        
        # Получаем метаданные файла
        file_stats = os.stat(file_path)
        
        # Формируем результат
        metadata = {
            "file_path": file_path,
            "title": file_name,
            "extension": file_extension,
            "size": file_stats.st_size,  # Размер файла в байтах
            "last_modified": datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),  # Последнее изменение
            "last_accessed": datetime.fromtimestamp(file_stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),  # Последний доступ
            "creation_time": datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),  # Время создания
            "mode": file_stats.st_mode,  # Режим файла
            "inode": file_stats.st_ino,  # Номер inode
            "device": file_stats.st_dev,  # Устройство
            "links": file_stats.st_nlink,  # Количество жестких ссылок
            "uid": file_stats.st_uid,  # Идентификатор пользователя
            "gid": file_stats.st_gid,  # Идентификатор группы
        }
        
        return [metadata]

    def _get_files_from_folder(self, folder):
        """
        Получает список всех файлов из указанной папки.
        """
        if not os.path.isdir(folder):
            raise NotADirectoryError(f"'{folder}' is not a directory.")
        
        # Получаем список всех файлов в папке
        files = [
            os.path.join(folder, f) for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]
        return files