from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task(10)
    def index(self):
        self.client.get("/")

    @task(1000)
    def get_config(self):
        self.client.get("/config?tenant=test_tenant&integration_type=test-information-type")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 10000