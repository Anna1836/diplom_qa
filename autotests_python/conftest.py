import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def browser():
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def payment_page(browser):
    wait = WebDriverWait(browser, 15)
    browser.get("http://localhost:8080/")

    buy_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Купить')]"))
    )
    buy_btn.click()

    return PaymentPage(browser)