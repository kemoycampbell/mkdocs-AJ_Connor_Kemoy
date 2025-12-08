import time
import json
import time
from locust import HttpUser, task, between, events
import random


class MkDocStressTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user think time between requests

    @task
    def load_homepage(self):
        self.client.get("/")
    
    @task
    def load_pages(self):
        pages = [
            "/getting-started/",
            "/nugets/",
            "/nethereum-managed-accounts/",
            "/nethereum-creating-a-new-account-using-geth/",
            "contracts/deploying/",
            "unity3d-smartcontracts-getting-started/",
        ]

        #randomly select a page to visit
        page = random.choice(pages)
        self.client.get(page)
        #randomly simulate a user reading time or time spent on the page
        time.sleep(random.uniform(0.5, 2))


