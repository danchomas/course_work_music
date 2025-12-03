import boto3
import os
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

class S3Client:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='s3',
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            region_name=os.getenv("S3_REGION_NAME"),
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

    def upload_file(self, file_obj, object_name):
        try:
            self.client.upload_fileobj(file_obj, self.bucket_name, object_name)
            return object_name
        except Exception as e:
            print(f"Ошибка загрузки в S3: {e}")
            raise e

    def generate_presigned_url(self, object_name, expiration=3600):
        try:
            response = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return response
        except Exception as e:
            print(f"Ошибка генерации ссылки: {e}")
            return None

    def delete_file(self, object_name):
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def get_file_object(self, object_name):
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=object_name)
            return response['Body']
        except Exception as e:
            print(f"Ошибка получения файла из S3: {e}")
            return None

s3 = S3Client()
