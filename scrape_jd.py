import asyncio
from playwright.async_api import async_playwright
import subprocess
from bs4 import BeautifulSoup

url = "https://ae.indeed.com/q-ai-ml-engineer-jobs.html?vjk=7f29000f62f7f273"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
selectors = {
                "JD":r"#jobDescriptionText",
                "title":r"#viewJobSSRRoot > div > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-81tydb.eu4oa1w0.hydrated > div.css-1yuy2sm.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-rndth6.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-rbjs5z.eu4oa1w0 > div:nth-child(1) > div.jobsearch-JobInfoHeader-title-container.css-1u3gzh9.eu4oa1w0",
                "company":r"#viewJobSSRRoot > div > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-81tydb.eu4oa1w0.hydrated > div.css-1yuy2sm.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-rndth6.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-rbjs5z.eu4oa1w0 > div:nth-child(1) > div.css-1xky5b5.eu4oa1w0 > div > div > div > div.css-oy1dfc.eu4oa1w0 > div.css-19qk8gi.eu4oa1w0",
                "location":r"#viewJobSSRRoot > div > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-81tydb.eu4oa1w0.hydrated > div.css-1yuy2sm.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-rndth6.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-rbjs5z.eu4oa1w0 > div:nth-child(1) > div.css-1xky5b5.eu4oa1w0 > div > div > div > div.css-89aoy7.eu4oa1w0"
            }

async def scrape_jd(page, url):
    await page.goto(url)
    await asyncio.sleep(3)  # allow content to load fully
    html =await page.content()
    soup = BeautifulSoup(html, "html.parser")
    results = {}
    for key, selector in selectors.items():
        el = soup.select_one(selector)
        results[key] = el.get_text(separator=" ",strip=True) if el else None

    return results

def open_chrome_with_debugging():
    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        r'--user-data-dir=C:\playwright\ChromeProfile'
    ])

def pretty_print_dict(d):
    for key, value in d.items():
        print(f"{key}:")
        print(value)
        print()

async def main():    
    async with async_playwright() as p:
        open_chrome_with_debugging()
        await asyncio.sleep(3)  # Give Chrome some time to start
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        await asyncio.sleep(3)
        job_details=await scrape_jd(page, url)
        pretty_print_dict(job_details)
        


if __name__ == "__main__":
    asyncio.run(main()) 