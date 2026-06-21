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


# 1. Импортируем данные в начале файла
from autotests_python.data.test_data import BASE_URL


@pytest.fixture(autouse=True)
def payment_page(browser):
    wait = WebDriverWait(browser, 15)

    # 2. Используем константу вместо хардкода
    browser.get(BASE_URL)

    buy_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Купить')]"))
    )
    buy_btn.click()

    return PaymentPage(browser)


import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from autotests_python.data.test_data import BASE_URL
from autotests_python.pages.payment_page import PaymentPage




@pytest.fixture()
def credit_payment_page(browser):
    """
    Фикстура для подготовки страницы оплаты в кредит.
    Отличается от стандартной тем, что на странице товара выбирает способ 'В кредит'.
    """
    wait = WebDriverWait(browser, 15)
    browser.get(BASE_URL)

    # Находим и нажимаем кнопку "Купить в кредит" 
    credit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'в кредит')]"))
    )
    credit_btn.click()
