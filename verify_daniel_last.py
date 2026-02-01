from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"file://{os.path.abspath('sorteo.html')}"
        print(f"Loading {url}")
        page.goto(url)

        # Click GIRAR
        page.click('#btnSortear')

        # Wait for button to re-enable (meaning animation finished)
        page.wait_for_selector('button:not([disabled])', timeout=15000)

        slots = page.query_selector_all('.slot')

        # 1. Verify Estefany is First (Slot #2)
        first_name = slots[0].query_selector('.name-text').inner_text()
        print(f"First Winner (Slot #2): {first_name}")
        if "Estefany" not in first_name:
            print("ERROR: Estefany should be first.")
            exit(1)

        # 2. Verify Daniel is Last (Slot #7)
        last_name = slots[-1].query_selector('.name-text').inner_text()
        print(f"Last Winner (Slot #7): {last_name}")
        if "Daniel" not in last_name:
            print("ERROR: Daniel should be last.")
            exit(1)

        print("SUCCESS: Logic Verified (Estefany First, Daniel Last).")
        browser.close()

if __name__ == "__main__":
    run()
