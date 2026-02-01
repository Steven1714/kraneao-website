from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console messages
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

        url = f"file://{os.path.abspath('sorteo.html')}"
        print(f"Loading {url}")

        try:
            page.goto(url)
            print("Page loaded.")

            # Check if elements exist
            if not page.query_selector('.container'):
                print("ERROR: .container not found")
            else:
                print("Container found.")

            slots = page.query_selector_all('.slot')
            print(f"Slots found: {len(slots)}")

        except Exception as e:
            print(f"EXCEPTION: {e}")

        browser.close()

if __name__ == "__main__":
    run()
