import threading
import time
import requests
from selenium import webdriver
import sys
from requests.auth import HTTPBasicAuth
from time import sleep
import os

num_parallel_threads = 1
def get_chrome_session_logs(session_id):
    response = requests.get("https://api.browserstack.com/automate/sessions/{}.json".format(session_id),
                            auth=HTTPBasicAuth(os.environ['BROWSERSTACK_USERNAME'], os.environ['BROWSERSTACK_ACCESS_KEY']))
    browser_console_log_url = response.json(
    )["automation_session"]["browser_console_logs_url"]
    response2 = requests.get(browser_console_log_url)
    print(response2.content)
class AutomateParallelThread(threading.Thread):
    def run(self):

        desired_cap = {
            'os' : 'Windows',
            'os_version' : '10',
            'browser' : 'Chrome',
            'resolution' : '1920x1080',
            'browserstack.local' : 'true',
            'build' : 'Akhil new',
            'browserstack.localIdentifier': os.environ['BROWSERSTACK_LOCAL_IDENTIFIER'],
            'browserstack.local' : os.environ['BROWSERSTACK_LOCAL'],
            'browserstack.console': 'verbose',
        }

        hub_url = "http://%s:%s@hub-cloud.browserstack.com:80/wd/hub" % (os.environ['BROWSERSTACK_USERNAME'], os.environ['BROWSERSTACK_ACCESS_KEY'])
        driver = webdriver.Remote(
            command_executor=hub_url,
            desired_capabilities=desired_cap)
        # start_time = time.time()
        start_time = time.time()

        driver.get("https://fast.com")

        end_time = time.time()

        print(driver.session_id)
        print("Execution time {}".format(end_time - start_time))

        driver.quit()

all_threads = []
for i in range(num_parallel_threads):
    automateThread = AutomateParallelThread()
    all_threads.append(automateThread)
for thread in all_threads:
    thread.start()
for thread in all_threads:
    thread.join()