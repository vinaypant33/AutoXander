from playwright.sync_api import sync_playwright






def main_working():
    with sync_playwright() as p:
        browser  = p.chromium.launch(headless=False , args=["--start-maximized"])
        page  = browser.new_page()




        # Wait for 8 seconds :: for browser to close
        page.wait_for_timeout(30000)



