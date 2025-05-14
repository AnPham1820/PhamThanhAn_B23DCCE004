import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

df = pd.read_csv("results.csv")
players_with_900_minutes = df[df['Minutes'] > 900]['Name'].str.strip().str.lower().tolist()
print("Number of players with Minutes > 900:", len(players_with_900_minutes))

chrome_options = Options()

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get("https://www.footballtransfers.com/us/leagues-cups/national/uk/premier-league/2024-2025")
wait = WebDriverWait(driver, 20)

results = []

try:
    full_list_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tab-content div.btm-link a')))
    href = full_list_link.get_attribute("href")
    if not href:
        raise Exception("Failed to retrieve href from <a> tag")

    found_players = set()

    for i in range(1, 23):
        paged_url = href if i == 1 else f"{href}/{i}"
        print(f"\nProcessing page: {paged_url}")

        retry_count = 0
        while retry_count < 3:
            try:
                driver.get(paged_url)
                time.sleep(10 if i == 1 else 3)

                wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, 'td.td-player')) > 0)

                table = driver.find_element(By.CSS_SELECTOR, 'table.mvp-table')
                tbody = table.find_element(By.TAG_NAME, 'tbody')
                rows = tbody.find_elements(By.TAG_NAME, 'tr')

                invalid_count = 0
                for row in rows:
                    try:
                        player_td = row.find_element(By.CSS_SELECTOR, 'td.td-player')
                        name = player_td.text.strip().split('\n')[0]
                        name_key = name.lower()
                        if name_key in players_with_900_minutes and name not in found_players:
                            value_td = row.find_element(By.CSS_SELECTOR, 'span.player-tag')
                            transfer_value = value_td.text

                            results.append({"Name": name, "ETV": transfer_value})
                            found_players.add(name)
                    except:
                        invalid_count += 1

                if invalid_count:
                    print(f"Skipped {invalid_count} invalid rows.")
                break 

            except Exception as e:
                retry_count += 1
                print(f"Error loading page (attempt {retry_count}) — retrying...")

        if retry_count == 3:
            print(f"Skipped page {i} after 3 failed attempts.")

except Exception as e:
    print("Error accessing main page or retrieving link:", e)

print(f"\nTotal matched players found: {len(found_players)}")

original_set = set(players_with_900_minutes)
found_set = set(name.lower() for name in found_players)

missing_players = original_set - found_set

print(f"\nNumber of players NOT found on the main page: {len(missing_players)}")
for missing in sorted(missing_players):
    print("⛔", missing.title())

for player in missing_players:
    print(f"Searching for: {player}")
    try:
        driver.get("https://www.footballtransfers.com")
        time.sleep(3)

        search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.fa.fa-search")))
        search_icon.click()

        search_panel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-panel")))

        search_box = search_panel.find_element(By.CSS_SELECTOR, "input")
        search_box.clear()
        search_box.send_keys(player)
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.searchResults a")))
        first_result = driver.find_element(By.CSS_SELECTOR, "div.searchResults a")

        player_name_elem = first_result.find_element(By.CSS_SELECTOR, "div.text b")
        player_name = player_name_elem.text.strip()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pl_value")))
        etv_value = driver.find_element(By.CSS_SELECTOR, "div.pl_value").text.strip()

        results.append({"Name": player_name, "ETV": etv_value})

    except Exception as e:
        print(f"Could not retrieve data for {player}: {e}")
        results.append({"Name": player, "ETV": "Not found"})

driver.quit()

print("\nFull list of players and their Estimated Transfer Value (ETV):")
for r in results:
    print(f"{r['Name']}: {r['ETV']}")

output_df = pd.DataFrame(results)

original_df = pd.read_csv("results.csv")
original_df["Name_Key"] = original_df["Name"].str.strip().str.lower()

output_df["Name_Key"] = output_df["Name"].str.strip().str.lower()

final_df = pd.merge(
    output_df,
    original_df[["Name_Key", "Age", "Position", "Goals", "Assists"]],
    on="Name_Key",
    how="left"
).drop(columns=["Name_Key"])

final_df.to_csv("results_bai_4.csv", index=True, encoding="utf-8-sig")
print("\nResults saved to 'results_bai_4.csv'")
