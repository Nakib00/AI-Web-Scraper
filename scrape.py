from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import random
import time

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

# List of user agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
]

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Use local ChromeDriver
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Mask selenium's presence
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def scrape_website(website, max_retries=3):
    print(f"Attempting to scrape {website}...")
    
    for attempt in range(max_retries):
        try:
            driver = setup_driver()
            
            # Add random delay before request
            time.sleep(random.uniform(2, 5))
            
            driver.get(website)
            
            # Wait for the body to be present
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Add random delay to simulate human behavior
            time.sleep(random.uniform(1, 3))
            
            html = driver.page_source
            driver.quit()
            return html
            
        except TimeoutException:
            print(f"Timeout on attempt {attempt + 1} of {max_retries}")
            if driver:
                driver.quit()
            if attempt == max_retries - 1:
                raise
            time.sleep(random.uniform(5, 10))
            
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {str(e)}")
            if driver:
                driver.quit()
            if attempt == max_retries - 1:
                raise
            time.sleep(random.uniform(5, 10))


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
