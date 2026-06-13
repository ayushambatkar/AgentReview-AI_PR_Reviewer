from locust import HttpUser, task

class RateLimiterUser(HttpUser):

    @task
    def hit_endpoint(self):
        self.client.get("/health")