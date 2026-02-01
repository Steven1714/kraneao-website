from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load local file
        url = f"file://{os.path.abspath('sorteo.html')}"
        print(f"Loading {url}")
        page.goto(url)

        # 1. Verify initial state (6 slots, numbering starts at #2)
        slots = page.query_selector_all('.slot')
        print(f"Found {len(slots)} slots.")
        if len(slots) != 6:
            print("ERROR: Expected 6 slots.")
            exit(1)

        first_number = slots[0].query_selector('.position-number').inner_text()
        print(f"First slot number: {first_number}")
        if first_number != "#2":
            print("ERROR: First slot should be #2")
            exit(1)

        # 2. Click GIRAR
        print("Clicking GIRAR...")
        page.click('#btnSortear')

        # 3. Wait for all to finish
        # The last one finishes after 1000 + 5 * 900 = 5500ms approx.
        # Let's wait for the button to be enabled again or check classes.
        print("Waiting for results...")
        page.wait_for_selector('button:not([disabled])', timeout=10000)

        # 4. Check results
        slots = page.query_selector_all('.slot')

        # Check Slot #2 (Index 0)
        winner_name = slots[0].query_selector('.name-text').inner_text()
        print(f"Position #2 Winner: {winner_name}")

        if "Estefany" not in winner_name:
            print("ERROR: Estefany should be in Position #2")
            exit(1)

        print("SUCCESS: Estefany is #2")

        # Check others
        other_names = []
        for i in range(1, 6):
            name = slots[i].query_selector('.name-text').inner_text()
            other_names.append(name)

        print(f"Other winners: {other_names}")
        expected_pool = {"Daniel", "Tato", "Amarilis", "Ricardo", "Celeida"}
        if set(other_names) == expected_pool:
             print("SUCCESS: All other participants are present.")
        else:
             print(f"ERROR: Participants mismatch. Expected {expected_pool}, got {set(other_names)}")
             exit(1)

        browser.close()

if __name__ == "__main__":
    run()
