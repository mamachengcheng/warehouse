from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    # def on_start(self):
    #     userAgent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36";
    #     self.client.request(method='post',url='/login/',headers={
    #         'referer': 'http://www.baidu.com',
    #         'user-agent':userAgent,
    #     },data={
    #         'username':'',
    #         'password':''
    #     })
        # self.client.post("/login/",{
        #     'username':'',
        #     'password':''
        # })

    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def backend(self):
        self.client.get("/admin/")

    @task(1)
    def login(self):
        self.client.post("login",{'username':'name','password':'name1234'})
    # @task(1)
    # def account_list(self):
    #     self.client.get("/account_list/")
    #
    # @task(1)
    # def level_list(self):
    #     self.client.get("/level_list/")

class User(HttpLocust):
    task_set = UserBehavior
    host = 'http://140.143.117.234/'
    min_wait = 1000
    max_wait = 3000
