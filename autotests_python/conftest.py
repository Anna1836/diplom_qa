import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 1. Импортируем веб-драйвер-менеджер для автоматического управления драйвером
from webdriver_manager.chrome import ChromeDriverManager

# 2. Импортируем константу с URL из отдельного модуля данных
from autotests_python.data.test_data import BASE_URL


# --- Фикстура для браузера (остается без изменений) ---
@pytest.fixture(scope="function")
def browser():
    """
    Фикстура для инициализации и закрытия браузера.
    Область видимости 'function' означает, что браузер будет открываться
    заново для каждого теста.
    """
    options = Options()
    # Добавьте любые нужные опции, например headless режим:
    # options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    yield driver  # Точка, где тест получает управление

    driver.quit()  # Код после yield выполнится после завершения теста


# --- Импортируем классы Page Object (делаем это здесь, чтобы избежать циклических импортов) ---
from autotests_python.pages.product_page import ProductPage
from autotests_python.pages.payment_page import PaymentPage


# --- Фикстура для стандартного сценария оплаты ---
@pytest.fixture(autouse=True)
def payment_page(browser):
    """
    Фикстура для подготовки страницы полной оплаты.
    Открывает главную страницу и переходит к форме оплаты.
    Автоматически используется во всех тестах, если не указано иное.
    """
    page = PaymentPage(browser)
    page.open()  # Навигация делегирована методу open() класса PaymentPage
    return page


# --- Фикстура для сценария покупки в кредит ---
@pytest.fixture()
def credit_payment_page(browser):
    """
    Фикстура для подготовки страницы оплаты в кредит.
    Отличается от стандартной тем, что на странице товара выбирает способ 'В кредит'.
    Эту фикстуру нужно явно указывать в параметрах теста, который ее использует.
    """
    # Переходим на главную страницу товара
    browser.get(BASE_URL)

    # Создаем объект страницы товара
    product_page = ProductPage(browser)

    # Используем бизнес-метод для выбора кредита, который возвращает готовую страницу оплаты
    return product_page.buy_in_credit()
