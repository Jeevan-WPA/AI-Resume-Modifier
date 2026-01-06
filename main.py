import scrape_jd
import resume_build
import os
from playwright.async_api import async_playwright
import asyncio
import shutil

url = "https://ae.indeed.com/viewjob?jk=3fc9a5b209927ea3&from=shareddesktop_copy"
src = "./resume_template"

async def main():    
    async with async_playwright() as p:
        chrome=scrape_jd.open_chrome_with_debugging()
        await asyncio.sleep(3)  # Give Chrome some time to start
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        await asyncio.sleep(3)
        job_details=await scrape_jd.scrape_jd(page, url)
        pretty_print_dict(job_details)
        
        scrape_jd.update_csv("./Jobs_Applied/jobs_applied.csv", job_details)
        
        job_description = job_details.get("JD", "")
        optimized_sections = resume_build.optimize_resume(job_description)
        
        dst= f"./Jobs_Applied/{job_details['company']}_{job_details['job_title']}_application_resume"
        
        if not os.path.exists(dst):
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
            "summary.tex",
            "experience.tex",
            "skills.tex",
                ),
            )
        else:
            print(f"Directory {dst} already exists. Overwriting the sections.")
            return
        
        for name in ("summary", "experience", "skills"):
            with open(f"{dst}/src/{name}.tex", "w") as f:
                f.write(optimized_sections[name])
        
        print(f"✓ Resume optimized and saved to {dst} directory")
        
        scrape_jd.save_as_pdf(f"{dst}/resume.tex", output_dir=dst)
        print(f"✓ PDF generated and saved to {dst} directory")
        
        await browser.close()
        chrome.terminate()
        
def pretty_print_dict(d):
    for key, value in d.items():
        print(f"{key}:")
        print(value)
        print()

    
if __name__ == "__main__":
    asyncio.run(main()) 