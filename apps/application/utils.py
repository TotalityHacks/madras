import asyncio
from pyppeteer import launch
from urllib.parse import urlparse

from django.conf import settings


async def screengrab_async(url):
    domain = urlparse(url).netloc

    browser = await launch()
    page = await browser.newPage()

    if "linkedin" in domain:
        await page.goto("https://linkedin.com/", {"waitUntil": "networkidle2"})
        await page.evaluate("""() => {{
            document.getElementById('login-email').value = '{}';
            document.getElementById('login-password').value = "{}";
            document.querySelector(".login-form").submit();
        }}""".format(settings.LINKEDIN_USERNAME, settings.LINKEDIN_PASSWORD))
        await page.waitForNavigation()

    await page.goto(url, {"waitUntil": "networkidle2"})

    height = await page.evaluate("""() => {
        return document.documentElement.scrollHeight;
    }""")
    await page.setViewport(viewport={"width": 1028, "height": height})
    buf = await page.screenshot()
    await browser.close()
    return buf


def screengrab(url):
    return asyncio.get_event_loop().run_until_complete(screengrab_async(url))
