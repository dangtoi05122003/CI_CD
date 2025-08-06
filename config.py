from selenium.webdriver.chrome.options import Options

def setup():
    options = Options()
    options.add_argument("--headless=chrome")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--remote-debugging-port=0")
    return options
