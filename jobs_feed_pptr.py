import json
import os
import asyncio
from pyppeteer import launch


async def get_job_list(page, jobs_data, last_job_link):
    await page.goto("https://www.upwork.com/nx/search/jobs/?nbs=1&q=python&page=1&per_page=50")

    await page.waitForSelector('.job-tile')

    jobs_articles = await page.querySelectorAll('.job-tile')

    print(len(jobs_articles))

    for job in jobs_articles:
        link_element = await job.querySelector('a')
        link = await page.evaluate('(element) => element.href', link_element)

        if link == last_job_link:
            break

        title_element = await job.querySelector('.job-tile-title')
        job_title_text = (await page.evaluate('(element) => element.textContent', title_element)).strip()

        description_element = await job.querySelector('.text-body-sm')
        job_description = (await page.evaluate('(element) => element.textContent', description_element)).strip()

        info_items = await job.querySelectorAll('.job-tile-info-list li')
        rate = (await page.evaluate('(element) => element.textContent', info_items[0])).strip() if len(
            info_items) > 0 else "N/A"
        exp_lvl = (await page.evaluate('(element) => element.textContent', info_items[1])).strip() if len(
            info_items) > 1 else "N/A"
        est_time = (await page.evaluate('(element) => element.textContent', info_items[2])).strip() if len(
            info_items) > 2 else "N/A"

        cleaner_est_time = est_time.split('\n', 1)[-1]

        tag_list = []
        tags = await job.querySelectorAll('.air3-token')
        for tag in tags[:8]:
            tag_text = (await page.evaluate('(element) => element.textContent', tag)).strip()
            tag_list.append(tag_text)

        job_obj = {
            "title": job_title_text,
            "description": job_description,
            "tags": tag_list,
            "rate": rate,
            "exp_lvl": exp_lvl,
            "est_time": cleaner_est_time,
            "link": link
        }

        jobs_data.append(job_obj)

    return jobs_data


async def find_jobs():
    jobs_output_file = "jobs_data.json"

    if os.path.exists(jobs_output_file):
        with open(jobs_output_file, "r") as file:
            existing_data = json.load(file)
            last_job_link = existing_data[0]["link"] if existing_data else None
    else:
        existing_data = []
        last_job_link = None

    jobs_data = []

    browser = await launch()
    page = await browser.newPage()

    jobs_data = await get_job_list(page, jobs_data, last_job_link)

    updated_data = jobs_data + existing_data

    with open(jobs_output_file, "w") as file:
        json.dump(updated_data, file, indent=4)

    print(f"Extracted data written to json")

    await browser.close()
