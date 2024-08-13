from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def main():
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get('https://hprera.nic.in/PublicDashboard')

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#reg-Projects"))
    )

    ref_numbers = driver.find_elements(By.CSS_SELECTOR, ".col-lg-9 #reg-Projects .form-row a")

    for i, ref in enumerate(ref_numbers[:6]):
        print(f"Processing item {i+1}...")
        res={}
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", ref)

            driver.execute_script("arguments[0].click();", ref)
            print("Card parsed")

            details_panel = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody.lh-2"))
            )

            table_html = details_panel.get_attribute('innerHTML')

            soup = BeautifulSoup(table_html, 'html.parser')

            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                Keys = [col.get_text(strip=True) for col in cols[0]]
                values=[col.get_text(strip=True) for col in cols[1]]
                key=Keys[0] # using hash maps to store key and value pairs
                res[key]=values
            print(f"Name:{res['Name']}\nPAN NO.:{res['PAN No.'][1]}\nPermanent address:f{res['Permanent Address'][1]}\nGSTIN NO:{res['GSTIN No.'][1]}")

            print("-" * 100)

        except Exception as e:
            print(f"Failed to extract details for item {i+1}: {e}")
            driver.save_screenshot(f"error_item_{i+1}.png")  # Take a screenshot for debugging

        driver.back()

    driver.quit()

if __name__ == "__main__":
    main()
