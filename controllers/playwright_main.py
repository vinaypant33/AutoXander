import json
import os
from pathlib import Path
from time import sleep
from playwright.sync_api import sync_playwright, TimeoutError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "config", "instructions.json")  # just to make the instructions availabel for this current file : 

INSTRUCTIONS_FILE = MODEL_PATH
POLL_INTERVAL = 60  # seconds


def load_instructions(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load instructions: {e}")
        return []


def highlight_element(page, selector):
    try:
        page.eval_on_selector(selector, """
        element => {
            element.style.transition = 'outline 0.3s ease';
            element.style.outline = '3px solid red';
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => { element.style.outline = ''; }, 1000);
        }
        """)
    except Exception as e:
        print(f"[WARN] Could not highlight selector {selector}: {e}")


def execute_instructions(page, instructions):
    for idx, step in enumerate(instructions):
        action = step.get("action")
        print(f"[{idx+1}] Action: {action}")

        try:
            if action == "goto":
                page.goto(step["url"])
            elif action == "click":
                selector = step["selector"]
                highlight_element(page, selector)
                page.click(selector, timeout=5000)
            elif action == "fill":
                selector = step["selector"]
                highlight_element(page, selector)
                page.fill(selector, step["value"])
            elif action == "wait":
                page.wait_for_timeout(step["seconds"] * 1000)
            elif action == "screenshot":
                path = step.get("path", f"output/screenshot_{idx+1}.png")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                page.screenshot(path=path)
            elif action == "extract_html":
                html = page.content()
                output_path = step.get("output", "output/page.html")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html)
            else:
                print(f"[WARN] Unknown action: {action}")
        except TimeoutError:
            print(f"[ERROR] Timeout for selector: {step.get('selector')}")
        except Exception as e:
            print(f"[ERROR] Failed step {idx+1}: {e}")


def get_current_page_source(page):
    try:
        html = page.content()
        output_path = "output/live_page_dump.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("[INFO] Page source saved to:", output_path)
        return html
    except Exception as e:
        print(f"[ERROR] Could not get page source: {e}")
        return None



def main_working():
    last_content = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context()
        page = context.new_page()

        while True:
            try:
                current_content = Path(INSTRUCTIONS_FILE).read_text()
                if current_content != last_content:
                    instructions = json.loads(current_content)
                    print("\n[INFO] Detected new instructions...")
                    execute_instructions(page, instructions)
                    last_content = current_content
                else:
                    print("[INFO] No change in instructions.")
            except Exception as e:
                print(f"[ERROR] JSON Read/Execution Failed: {e}")
            sleep(POLL_INTERVAL)


# if __name__ == "__main__":
#     main_working()
