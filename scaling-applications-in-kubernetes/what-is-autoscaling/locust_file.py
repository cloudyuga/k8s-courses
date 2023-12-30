# locust_file.py
import time
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def check_page(self):
        self.client.get(url="/")
