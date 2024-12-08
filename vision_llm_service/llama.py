from ollama import chat
from PyPDF2 import PdfReader

class LlamaModel:
    """
    Класс для использования LLaMA через библиотеку Ollama.
    """

    def __init__(self, model_name: str = "llama3.1:8b-instruct-q8_0"):
        """
        Инициализация модели LLaMA через Ollama.

        :param model_name: Название модели в Ollama
        """
        self.model_name = model_name

    def generate_text(self, user_text: str, combined_content: str) -> str:
        """
        Генерация текста с помощью Ollama.

        :param user_text: Текст запроса пользователя
        :param combined_content: Текст из всех PDF с указанием источников
        :return: Сгенерированный текст
        """
        prompt = f"""
        Вы — интеллектуальный помощник, ваша задача — анализировать содержимое, извлеченное из нескольких PDF-файлов, и отвечать на заданный пользователем вопрос или семантический запрос. 
        Каждый файл помечен своим именем. 
        Ваша задача: 1. Если вопрос пользователя (user_text) касается содержания какого-либо файла, предоставьте краткий и релевантный ответ для каждого файла. 
        2. Если файл не содержит информации, связанной с вопросом, пропустите его. 
        Формат ответа: - Начинайте с "В файле 'имя_файла':" и укажите ответ на вопрос пользователя. - Пропускайте файлы, которые не содержат релевантной информации. 
        Входные данные: - user_text: "{user_text}" - combined_content: "{combined_content}" Ответ должен быть точным и лаконичным."
        """
        print(f'prompt {prompt}')
        try:
            response = chat(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model_name
            )
            print(f'response prompt {response["message"]["content"].strip()}')
            return response["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate text using Ollama: {str(e)}")

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Извлечение текста из PDF-файла.

        :param file_path: Путь к PDF-файлу
        :return: Извлеченный текст
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    def summary(self, user_text: str, combined_content: str) -> str:
        """
        Формирование краткого содержания для каждого файла отдельно.

        :param combined_content: Текст из llama анализа
        :return: Краткое содержание с разбивкой по файлам
        """
        prompt = f"""
        Вы — умный ассистент. Ваша задача — ответить на заданный пользователем вопрос, используя содержимое, извлеченное из нескольких PDF-файлов. Каждый файл помечен своим именем. 
        Инструкции: 1. Ознакомьтесь с вопросом пользователя (user_text) и содержимым файлов (combined_content). 
        2. Найдите релевантную информацию в содержимом файлов. 
        3. Предоставьте краткий и точный ответ на вопрос, основываясь на информации из файлов. 
        4. Если вопросу нет подходящего ответа в содержимом, сообщите: "В предоставленных файлах ответа на вопрос не найдено." 
        Входные данные: - Вопрос: "{user_text}" - Содержимое файлов: "{combined_content}" Ответ должен быть лаконичным, точным и содержать только необходимую информацию..
        
        Содержимое:
        {combined_content}

        Предоставьте резюме для каждого файла ниже:
        """
        try:
            response = chat(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model_name
            )
            return response["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate summary using Ollama: {str(e)}")