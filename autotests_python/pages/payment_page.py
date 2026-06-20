from typing import Any, List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class PaymentPage:
    """
    Класс-описание страницы оплаты.
    Инкапсулирует все локаторы и методы для взаимодействия с элементами страницы.
    """

    # --- КОНСТАНТЫ СЕЛЕКТОРОВ ---
    # Все локаторы вынесены сюда. Если они изменятся на сайте, правим только здесь.
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")
    CARD_HOLDER_FIELD = (
        By.XPATH,
        "//span[contains(text(), 'Владелец')]/parent::*/..//input"
    )
    CVC_FIELD = (By.CSS_SELECTOR, "input[placeholder='999']")
    CVC_FIELD_ANCHOR = (By.CSS_SELECTOR, "input[placeholder='999']")
    DATE_FIELDS = (By.CSS_SELECTOR, "input[placeholder='08'], input[placeholder='22']")
    SUBMIT_BUTTON = (By.XPATH, ".//button[.//span[text()='Продолжить']]")

    ERROR_MESSAGE = (
        By.XPATH,
        ".//span[contains(@class, 'error-message') "
        "or contains(text(), 'Истёк') "
        "or contains(text(), 'Неверный формат') "
        "or contains(text(), 'Обязательно')]"
    )

    def __init__(self, driver: Any) -> None:
        """
        Инициализация страницы.
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    # --- УТИЛИТНЫЙ МЕТОД ДЛЯ ОЖИДАНИЯ ---
    def _wait_for_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Явное ожидание видимости элемента.
        :param locator: Кортеж локатора (By, value).
        :param timeout: Таймаут ожидания в секундах. Если None, используется дефолтный.
        :return: Найденный WebElement.
        """
        wait_to_use = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait_to_use.until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент не найден или не виден на странице: {locator}"
        )

    # --- МЕТОДЫ ДЛЯ ВЗАИМОДЕЙСТВИЯ С ФОРМОЙ ---

    def fill_card_number(self, number: str) -> None:
        """Вводит номер карты в соответствующее поле."""
        field = self._wait_for_element(self.CARD_NUMBER_FIELD)
        field.clear()
        field.send_keys(number)



    def fill_holder(self, holder: str) -> None:
        """Вводит имя владельца карты."""
        field = self._wait_for_element(self.CARD_HOLDER_FIELD)
        field.clear()
        field.send_keys(holder)

    def fill_cvc(self, cvc: str) -> None:
        """Вводит CVC/CVV код."""
        field = self._wait_for_element(self.CVC_FIELD)
        field.clear()
        field.send_keys(cvc)


    def fill_date(self, month: str, year: str) -> None:
        """Вводит срок действия карты (месяц и год)."""
        # Находим все поля даты
        fields: List[WebElement] = self.wait.until(
            EC.presence_of_all_elements_located(self.DATE_FIELDS)
        )

        for field in fields:
            placeholder = field.get_attribute("placeholder")
            if placeholder in ['ММ', '08']:
                 field.send_keys(month)
            elif placeholder in ['ГГ', '22']:
                 field.send_keys(year)



    def submit(self) -> None:
        """Отправляет форму оплаты."""
        btn = self._wait_for_element(self.SUBMIT_BUTTON)
        # Прокрутка к элементу для надежности клика
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

    #--- МЕТОДЫ ДЛЯ ПРОВЕРКИ РЕЗУЛЬТАТОВ ---

    def get_error_message_text(self) -> str:
        """
        Возвращает текст сообщения об ошибке.
        Инкапсулирует логику поиска и ожидания элемента с ошибкой.
        :return: Текст ошибки.
        """
        error_element = self._wait_for_element(self.ERROR_MESSAGE)
        return error_element.text
    def get_error_message_element(self) -> WebElement:
        """
        Возвращает сам элемент с ошибкой.
        Это полезно, если нужно проверить не только текст, но и видимость или другие свойства.
        :return: WebElement с ошибкой.
        """
        return self._wait_for_element(self.ERROR_MESSAGE)
