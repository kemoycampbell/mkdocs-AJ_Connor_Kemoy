"""
Locust load tests for MkDocs serve command.
Since the mkdocs serve command is not intended for production,
these tests simulate a single user sequentially accessing multiple
pages with realistic wait times as if they were checking each page
during development, as well as all pages being loaded at once.
"""
from time import sleep
from locust import HttpUser, task, between

PAGES = [
    "/",
    "/getting-started/",
    "/nugets/",
    "/nethereum-managed-accounts/",
    "/nethereum-creating-a-new-account-using-geth/",
    "/contracts/deploying/",
    "/unity3d-smartcontracts-getting-started/",
]

class MkDocsUserSeq(HttpUser):
    # Assuming pages are moderately sized and user reads sequentially
    # Simulate a single user checking a page every 30-60 seconds
    wait_time = between(30, 60)
    current_page = 0

    @task
    def load_page(self):
        # Request the current page
        self.client.get(PAGES[self.current_page])
        # Move to the next page for the next request
        self.current_page += 1
        if self.current_page >= len(PAGES):
            self.current_page = 0

class MkDocsUserOne(HttpUser):
    """
    This user is replicated to load all pages at once.
    The number of users should equal the number of pages, and they
    should be spawned at a high rate to simulate all pages loading simultaneously.
    """

    # Static variable to help assign pages to users
    current_page = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_to_load = MkDocsUserOne.current_page
        MkDocsUserOne.current_page += 1

    @task
    def load_page(self):
        """Load the assigned page."""
        self.client.get(PAGES[self.page_to_load])
        sleep(2000) # Sleep to prevent further requests
