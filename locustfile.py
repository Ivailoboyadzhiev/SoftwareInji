from locust import HttpUser, task, between

class FileStorageUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health_check(self):
        self.client.get("/health")

    @task
    def list_files(self):
        self.client.get("/files")

    @task
    def upload_file(self):
        file_data = {"file": ("locust_test.txt", b"Load test content", "text/plain")}
        self.client.post("/files", files=file_data)
