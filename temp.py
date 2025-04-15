from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from selenium.webdriver.edge.options import Options


# Initialize WebDriver
 
driver = webdriver.Edge()





#https://geomartcloud-enterprise-qa.nonprod.pge.com/portal/sharing/oauth2/approve?oauth_state=aFki8CHjKt_89Z-cGZ407Rw..YNgqeyXUVTEZZH9dslXOexYnUxsneyQmWWbllWmf015F4bOxkd7RcDgwgzOPjrjzHzMS5Zr0-N3hAsNLb_sZp75SHDITwHGqjdVylddSVKEYyNhIfbEcauaf_INHtfe_poNRb12Uhbk-oLGgTihJV91gnKzhvj8vZEIvk7MzUDxGvVGuvv6mM4vOwalq5SIwSoO0QkORNx-Pa5Sww1ltp8q9Vq6n0Lnr7MUDrP5uMbaVROTZrrCV8hdBmnGERpCXzUDB81L_T6BWWwfjye39fHkjZp3WXSa5vBbIoBFca5UY8H1basKPsd6ovyZ-WbU_tIQaO7ZocAmnItf9JjhoBNqOAF5Ih-DH3M8Y5yDP_-RiDdbdt3b69xYc34wn5Vmf1poxnsxtte4MAfVJFkdIgSwv1RoGDQSeKDaxFKxxCRelrWwEczXbqaHGKhU.
try:
    # Open the URL
    driver.get("https://pgenhydroviewerqa.nonprod.pge.com/")

    time.sleep(1000)

    


    # Wait for the pop-up and click the "OK" button
    # Wait for the pop-up and click the "OK" button
    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='dijitReset dijitInline dijitButtonText' and text()='OK']"))
    )
    time.sleep(5)
    ok_button.click()

    # Switch to the newly opened windo
    time.sleep(20)

except Exception as e:
    print(f"Error details: {e}")
        

finally:
    # Close the browser
    driver.quit()
