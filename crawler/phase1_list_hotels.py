import time, random, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

sys.stdout.reconfigure(encoding="utf-8")


def run_phase1():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    driver.get("https://www.ivivu.com/khach-san-ha-noi")
    time.sleep(6)

    hotels = []
    MAX_HOTELS = 10

    while len(hotels) < MAX_HOTELS:
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "iv-product-view"))
        )
        cards = driver.find_elements(By.CSS_SELECTOR, "iv-product-view")

        for c in cards:
            if len(hotels) >= MAX_HOTELS:
                break
            try:
                name = c.find_element(By.CSS_SELECTOR, ".pdv__hotel--name").text.strip()
                link = c.find_element(By.TAG_NAME, "a").get_attribute("href")
                stars = len(c.find_elements(By.CSS_SELECTOR, ".ivv-star-full-icon"))

                try:
                    point = c.find_element(By.CSS_SELECTOR, ".rtb__point-number").text
                except:
                    point = ""

                # ✅ GIÁ TRUNG BÌNH
                try:
                    avg_price = c.find_element(
                        By.CSS_SELECTOR, ".pdv__price-text-ta"
                    ).text
                except:
                    avg_price = "N/A"

                hotels.append(
                    {
                        "name": name,
                        "link": link,
                        "stars": stars,
                        "point": point,
                        "avg_price": avg_price,
                    }
                )

            except:
                continue

        try:
            btn = driver.find_element(By.CSS_SELECTOR, ".rgc__view-more-btn")
            driver.execute_script("arguments[0].scrollIntoView()", btn)
            btn.click()
            time.sleep(random.uniform(5, 8))
        except:
            break

    driver.quit()

    with open("data/hotel_links.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

    print(f"✅ Phase 1 done: {len(hotels)} hotels")
