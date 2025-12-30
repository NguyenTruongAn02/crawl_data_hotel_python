import json, time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

sys.stdout.reconfigure(encoding="utf-8")

def run_phase2():
    with open("data/hotel_links.json", encoding="utf-8") as f:
        hotels = json.load(f)

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    results = []

    for i, h in enumerate(hotels):
        print(f"[{i+1}/{len(hotels)}] {h['name']}")
        driver.get(h["link"])
        time.sleep(random.uniform(6, 10))

        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "iv-detail-room-class")
                )
            )
            room_blocks = driver.find_elements(By.CSS_SELECTOR, "iv-detail-room-class")
        except:
            print("⚠ Không load được phòng")
            continue

        rooms = []

        for r in room_blocks:
            try:
                name = r.find_element(By.CSS_SELECTOR, ".rccf__text--room-name").text

                try:
                    area = r.find_element(
                        By.XPATH,
                        ".//i[contains(@class,'ivv-area')]/following-sibling::span",
                    ).text
                except:
                    area = ""

                try:
                    price = r.find_element(
                        By.CSS_SELECTOR, ".left__currency.sale-price"
                    ).text
                except:
                    price = "N/A"

                rooms.append({"room_name": name, "area": area, "price": price})

            except:
                continue

        results.append({**h, "rooms": rooms})

    driver.quit()

    with open("data/hotel_full_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("✅ Phase 2 done")
