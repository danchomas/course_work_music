import os
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_DISK_OAUTH_TOKEN")
DB_URL = os.getenv("DATABASE_URL")
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

def create_postgres_backup():
    from urllib.parse import urlparse
    parsed = urlparse(DB_URL)
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    username = parsed.username
    database = parsed.path[1:]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dump_file = BACKUP_DIR / f"backup_{timestamp}.sql"

    env = os.environ.copy()

    cmd = [
        "pg_dump",
        "-h", host,
        "-p", str(port),
        "-U", username,
        "-d", database,
        "-f", str(dump_file),
        "--clean", "--no-owner", "--no-privileges"
    ]

    try:
        subprocess.run(cmd, env=env, check=True)
        print(f"✅ Бекап создан: {dump_file}")
        return dump_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка создания бекапа: {e}")
        return None

def upload_to_yandex_disk(local_path: Path):
    if not YANDEX_TOKEN:
        print("⚠️ Токен Яндекс.Диска не задан — загрузка пропущена")
        return

    file_name = local_path.name
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": f"OAuth {YANDEX_TOKEN}"}
    params = {"path": f"/backups/{file_name}", "overwrite": "true"}

    # Получаем ссылку для загрузки
    r = requests.get(upload_url, headers=headers, params=params)
    if r.status_code != 200:
        print(f"❌ Не удалось получить ссылку для загрузки: {r.text}")
        return False

    href = r.json().get("href")
    if not href:
        print("❌ Нет ссылки для загрузки")
        return False

    # Загружаем файл
    with open(local_path, "rb") as f:
        r2 = requests.put(href, files={"file": f})
        if r2.status_code == 201:
            print(f"✅ Файл загружен на Яндекс.Диск: {file_name}")
            return True
        else:
            print(f"❌ Ошибка загрузки: {r2.text}")
            return False

if __name__ == "__main__":
    backup_file = create_postgres_backup()
    if backup_file:
        upload_to_yandex_disk(backup_file)
