"""Locust spike test for MkDocs serve command."""
from locust import HttpUser, task, between


class MkDocsUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def load_homepage(self):
        self.client.get("/")
