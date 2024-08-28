from selenium import webdriver
from job_feed import find_jobs

options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)

find_jobs(browser=browser)
