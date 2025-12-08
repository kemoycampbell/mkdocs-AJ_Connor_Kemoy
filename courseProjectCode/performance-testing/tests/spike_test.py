"""Locust spike test for MkDocs serve command."""
from locust import HttpUser, task, between, LoadTestShape


class MkDocsUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def load_homepage(self):
        self.client.get("/")


class SpikeTestShape(LoadTestShape):
    """
    Spike Test:
      0–30 seconds: 25 users
      30–90 seconds: 125 users
      90–end: 25 users
    """

    def tick(self):
        run_time = self.get_run_time()

        # 0 - 30 seconds: warm-up
        if run_time < 30:
            return (25, 25)

        # 30 - 90 seconds: SPIKE
        elif run_time < 90:
            return (125, 125)

        # 90+ seconds: cool-down
        elif run_time < 120:
            return (25, 25)

        #end the test
        else:
            return None
