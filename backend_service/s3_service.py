import asyncio
from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from typing import TypedDict
from uuid import uuid4

from aiobotocore.session import get_session
from fastapi import UploadFile


def create_upload_file_from_path(file_path: Path) -> UploadFile:
    # Убедитесь, что путь существует и файл доступен
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    # Чтение содержимого файла
    with file_path.open("rb") as f:
        file_content = f.read()

    # Создаем объект UploadFile
    upload_file = UploadFile(
        filename=file_path.name,  # Имя файла
        file=BytesIO(file_content),  # Содержимое файла
    )
    return upload_file


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "verify": False,  # Отключить проверку SSL
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file: UploadFile,
            filename: str,
    ):
        async with self.get_client() as client:
            response = await client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file.file,
            )
            assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
            print(response)

    async def delete_file(self, object_name: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)
            print(f"File {object_name} deleted from {self.bucket_name}")

    async def get_file(self, object_name: str, destination_path: str):
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
            data = await response["Body"].read()
            with open(destination_path, "wb") as file:
                file.write(data)
            print(f"File {object_name} downloaded to {destination_path}")


S3_ACCESS = "732f0562a2c14c75aef611f713bf1e12"
S3_SECRET = "67a2c8a3ab994aba8225ec8fcdfba44a"
S3_URL = "https://s3.storage.selcloud.ru"
S3_BUCKET = "talent-people"
S3_SERVER = "https://6e634e1e-ad6b-40dd-85b8-55e222e730b5.selstorage.ru"


class FileRepo:
    def __init__(
            self,
            access_key: str = S3_ACCESS,
            secret_key: str = S3_SECRET,
            endpoint_url: str = S3_URL,
            bucket_name: str = S3_BUCKET,
    ):
        self._client = S3Client(access_key, secret_key, endpoint_url, bucket_name)

    def save_one(self, path: Path) -> str:
        file = create_upload_file_from_path(path)
        filename = str(uuid4()) + file.filename
        coro = self._client.upload_file(file, filename)
        asyncio.run(coro)
        return f"{S3_SERVER}/{filename}"


# {
#         "content": "Hello",
#         "sources": [{
#             "title": "First",
#             "src": src,
#             "pages": [1],
#         }]
#     }


class Source(TypedDict):
    title: str
    src: str
    pages: list[str]


class Data(TypedDict):
    content: str
    sources: list[Source]


def convert(data: Data) -> Data:
    sources = data["sources"]
    result_sources = []
    repo = FileRepo()
    for item in sources:
        link = repo.save_one(Path(item["src"]))
        result_sources.append(
            Source(title=item["title"], src=link, pages=item["pages"])
        )
    return Data(content=data["content"], sources=result_sources)
