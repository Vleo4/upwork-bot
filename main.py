from selenium import webdriver
from job_feed import find_jobs

options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
browser = webdriver.Chrome(options=options)

find_jobs(browser=browser)
