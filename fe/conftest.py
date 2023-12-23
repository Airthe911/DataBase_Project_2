# import requests
# import threading
# from urllib.parse import urljoin
# from be import serve
# from fe import conf

# thread: threading.Thread = None


# 修改这里启动后端程序，如果不需要可删除这行代码
# def run_backend():
#     rewrite this if rewrite backend
#     serve.be_run()


# def pytest_configure(config):
#     global thread
#     print("frontend begin test")
#     thread = threading.Thread(target=run_backend)
#     thread.start()


# def pytest_unconfigure(config):
#     url = urljoin(conf.URL, "shutdown")
#     requests.get(url)
#     thread.join()
#     print("frontend end test")


# 使用django框架，无需此处自动启动后端，在BookstoreDjango下，使用python manage.py runserver启动后端服务器