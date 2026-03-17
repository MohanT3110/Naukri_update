import os
import time
import schedule
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()
NAUKRI_USERNAME = os.getenv("NAUKRI_USERNAME")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
USER_NAME = os.getenv("USER_NAME")

# Check if credentials are set
if not NAUKRI_USERNAME or not NAUKRI_PASSWORD:
    raise ValueError("Naukri username or password not found in .env file. Please set them.")

NAUKRI_LOGIN_URL = "https://login.naukri.com/"
NAUKRI_PROFILE_URL = "https://www.naukri.com/mnjuser/profile"


def update_naukri_profile():
    """
    This function logs into Naukri, navigates to the profile page,
    and updates the 'Profile Name' to refresh the profile's 'last updated' timestamp.
    """
    print("--- Starting Naukri Profile Update ---")
    driver = None  # Initialize driver to None
    try:
        # --- 1. Initialize WebDriver ---
        options = webdriver.ChromeOptions()
        
        # REQUIRED FOR ARM / ORACLE CLOUD: Point to the system-installed Chromium
        options.binary_location = '/usr/bin/chromium-browser'
        
        options.add_argument("--headless")  # Server environment requires headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # REQUIRED FOR ARM: Use the system-installed chromedriver
        service = ChromeService(executable_path='/usr/bin/chromedriver')
        
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20) # Set a generous wait time

        # --- 2. Login to Naukri ---
        print("Navigating to login page...")
        driver.get(NAUKRI_LOGIN_URL)
        
        print("Entering credentials...")
        # Find username field and enter username
        username_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        username_field.send_keys(NAUKRI_USERNAME)
        
        # Find password field and enter password
        password_field = driver.find_element(By.ID, "passwordField")
        password_field.send_keys(NAUKRI_PASSWORD)
        
        # Click the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for login to complete by checking for a known element on the homepage
        print("Pausing for 10 seconds after login click to observe...")
        time.sleep(10) 
        print("Login successful!")
        
        # --- 3. Navigate to Profile Page and Update ---
        print("Navigating to profile page...")
        driver.get(NAUKRI_PROFILE_URL)
        
        print("Looking for 'Profile Handler' to edit...")

        wait = WebDriverWait(driver, 10)
        edit_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//em[text()='editOneTheme']")))
        edit_icon.click()

        print("Clicked on edit icon.")
        time.sleep(5)

        # Find the name field using an attribute selector
        name_input = driver.find_element(By.CSS_SELECTOR, "input[value='Mohanraj T']")
        
        # Interact with it
        if name_input.is_displayed():
            print("Input field is visible.")
            name_input.clear() 
            time.sleep(5)
            name_input.send_keys("Mohanraj T")
            time.sleep(5)
        else:
            print("Input field is not visible.")
        
        # Click the save button
        save_button = driver.find_element(By.XPATH, "//button[text()='Save']")
        save_button.click()

        print("✅ Profile updated successfully!")
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ An error occurred: {e}")
        print("Could not update profile. This might be due to a website change, a CAPTCHA, or a slow connection.")
            
    finally:
        # --- 4. Clean Up ---
        if driver:
            print("Closing the browser.")
            driver.quit()
        print("--- Update process finished. Waiting for next schedule. ---\n")


# --- Execution ---
if __name__ == "__main__":
    print("🚀 Naukri Profile Updater Bot Started!")
    # Run the job once and then exit
    update_naukri_profile()
    print("✅ Execution completed. Exiting to free up memory.")