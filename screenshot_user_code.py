from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"file://{os.path.abspath('sorteo.html')}"
        page.goto(url)

        # Click and wait
        page.click('#btnSortear')
        page.wait_for_selector('button:not([disabled])', timeout=10000)

        page.screenshot(path='sorteo_user_final.png')
        print("Screenshot saved to sorteo_user_final.png")
        browser.close()

if __name__ == "__main__":
    run()
