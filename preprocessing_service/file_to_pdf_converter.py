import os
import time
import shutil
import subprocess
import requests
from PyPDF2 import PdfReader, PdfWriter

class FileToPdfConverter:
    def __init__(self):
        pass

    def convert(self, file_path, output_pdf_path):
        """
        Определяет тип файла и вызывает соответствующий метод для конвертации.
        """
        ext = self.get_file_extension(file_path)
        if ext in [".ppt", ".pptx", ".doc", ".docx"]:
            self.print_to_pdf(file_path, output_pdf_path)
        elif ext in ['.pdf', ".png", ".jpg", ".jpeg"]:
            self.move_to_directory(file_path, output_pdf_path)
        else:
            raise ValueError(f"Формат {ext} не поддерживается для конвертации в PDF.")

    def get_file_extension(self, file_name):
        """
        Возвращает расширение файла.
        """
        _, ext = os.path.splitext(file_name)
        return ext.lower()

    def print_to_pdf(self, file_path, output_pdf_path):
        """
        Конвертирует Word или PowerPoint файл в PDF с помощью LibreOffice на Windows.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        libreoffice_path = shutil.which("soffice") or r"C:\Program Files\LibreOffice\program\soffice.exe"

        if not os.path.exists(libreoffice_path):
            raise FileNotFoundError(f"LibreOffice не найдено по пути: {libreoffice_path}. Убедитесь, что оно установлено.")

        try:
            command = [
                libreoffice_path, "--headless", "--convert-to", "pdf",
                "--outdir", os.path.dirname(output_pdf_path), file_path
            ]
            subprocess.run(command, check=True)
            print(f"Файл успешно сохранён в PDF: {output_pdf_path}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ошибка при конвертации {file_path} в PDF: {e}")

    def split_pdf_pages(self, pdf_path, output_directory):
        """
        Разделяет PDF на отдельные страницы, сохраняя их в output_directory.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF файл {pdf_path} не найден.")

        pdf_reader = PdfReader(pdf_path)
        title = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.join(output_directory, title)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for page_num, page in enumerate(pdf_reader.pages, start=1):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)

            output_page_path = os.path.join(output_folder, f"{title}_{page_num}.pdf")
            with open(output_page_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

            print(f"Страница {page_num} сохранена как {output_page_path}.")

    def move_to_directory(self, file_path, target_directory):
        """
        Перемещает файлы PDF и изображения в указанную директорию.
        """
        try:
            shutil.copy(file_path, target_directory)
            print(f"Файл {file_path} перемещён в {target_directory}")
        except Exception as e:
            print(f"Ошибка при перемещении {file_path}: {e}")

    def clean_directory(self, directory_path):
        """
        Удаляет все файлы в указанной директории.
        """
        if os.path.exists(directory_path):
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Ошибка при удалении {file_path}: {e}")
        else:
            os.makedirs(directory_path)
            print(f"Директория {directory_path} создана.")

    def send_indexing_request(self, url):
        """
        Отправляет HTTP-запрос на указанный URL с заголовками Content-Type: application/json.
        """
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"Запрос на {url} успешно выполнен.")
            else:
                print(f"Запрос на {url} завершился с кодом: {response.status_code}. Ответ: {response.text}")
        except Exception as e:
            print(f"Ошибка при выполнении запроса на {url}: {e}")

    def monitor_and_convert(self, input_dir, output_dir, cut_pdf_dir):
        """
        Следит за файлами в input_dir и конвертирует их в PDF, сохраняя в output_dir.
        """
        print(f"Мониторинг папки: {input_dir}")
        processed_files = set()

        while True:
            # Получаем список файлов в директории
            current_files = {f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))}
            new_files = current_files - processed_files  # Определяем новые файлы

            if new_files:
                print(f"Найдены новые файлы: {new_files}")
                for file_name in new_files:
                    file_path = os.path.join(input_dir, file_name)
                    output_file_name = os.path.splitext(file_name)[0] + ".pdf"
                    output_file_path = os.path.join(output_dir, output_file_name)

                    try:
                        print(f"Обрабатываю файл: {file_path}")
                        self.convert(file_path, output_file_path)
                        print(f"Сохранено: {output_file_path}")
                        processed_files.add(file_name)  # Помечаем файл как обработанный

                        # Разделить PDF на страницы
                        self.split_pdf_pages(output_file_path, cut_pdf_dir)
                    except Exception as e:
                        print(f"Ошибка при обработке {file_path}: {e}")

                # Все новые файлы обработаны, вызываем индексацию
                print("Все новые файлы обработаны. Отправляю запрос в vllm_service.")
                #indexing_url = "http://127.0.0.1:8000/indexing"
                indexing_url = "http://backend_service:8000/indexing"
                self.send_indexing_request(indexing_url)
            else:
                print("Новых файлов не найдено. Ожидаю...")

            time.sleep(5)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(BASE_DIR, "samples")
output_directory = os.path.join(BASE_DIR, "results")
cut_pdf_directory = os.path.join(BASE_DIR, "cut_pdf")

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

if not os.path.exists(cut_pdf_directory):
    os.makedirs(cut_pdf_directory)

converter = FileToPdfConverter()
converter.monitor_and_convert(input_directory, output_directory, cut_pdf_directory)