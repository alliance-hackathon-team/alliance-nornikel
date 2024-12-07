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
        You are a smart assistant tasked with analyzing PDF content provided by the user. The user has provided two inputs:
        1. user_text - the input from the user, which can be a word, a set of words, a question, or a semantic query.
        2. combined_content - content extracted from multiple PDF files, where each file's content is labeled by its file name.

        Your task is as follows:
        - user_text is a question or a semantic query, provide a direct and concise answer for each relevant file. If a file does not contain relevant information, skip it.

        Respond in the following format:
        - For each file, start with "In file 'filename':" followed by the answer.
        - Skip files without relevant content.

        Here are the inputs:
        - user_text: "{user_text}"
        - combined_content: "{combined_content}"
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

    def summary(self, combined_content: str) -> str:
        """
        Формирование краткого содержания для каждого файла отдельно.

        :param combined_content: Текст из llama анализа
        :return: Краткое содержание с разбивкой по файлам
        """
        prompt = f"""
        Вы — ассистент, который составляет краткое содержание содержимого из нескольких помеченных источников.
        - Для каждого файла предоставьте краткое содержание на русском языке, даже если исходное содержание на другом языке.
        - Сохраните ключевые идеи и основное значение без лишних деталей.
        - Убедитесь, что каждое резюме помечено именем соответствующего файла.
        
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