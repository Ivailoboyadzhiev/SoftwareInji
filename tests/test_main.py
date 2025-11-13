import os
import sys

# Ensure Python can import main.py from the parent directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import app
from fastapi.testclient import TestClient
from pathlib import Path

client = TestClient(app)
STORAGE_DIR = Path("storage")


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "File Storage API" in response.json()["message"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_store_file():
    file_content = b"Hello, world!"
    response = client.post(
        "/files",
        files={"file": ("test.txt", file_content, "text/plain")},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
    assert (STORAGE_DIR / "test.txt").exists()


def test_list_files():
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert isinstance(data["files"], list)


def test_get_file():
    file_path = STORAGE_DIR / "test.txt"
    if not file_path.exists():
        file_path.write_text("data")

    response = client.get("/files/test.txt")
    assert response.status_code == 200
