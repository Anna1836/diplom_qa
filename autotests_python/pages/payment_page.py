
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


    # def fill_date(self, month: str, year: str) -> None:
    #
    # """Вводит срок действия карты (месяц и год)."""
    #         # Ждем, пока появятся ВСЕ элементы, найденные по локатору
    #         fields = self._wait_for_element(self.DATE_FIELDS)
    #         # Примечание: _wait_for_element с presence_of_all_elements_located вернет список
    #
    #         for field in fields:
    #             placeholder = field.get_attribute("placeholder")
    #
    #             # Проверяем, активен ли элемент (is_enabled), чтобы избежать проблем с readonly полями
    #             if field.is_enabled():
    #                 if placeholder in ['MM', '08']:
    #                     field.clear()
    #                     field.send_keys(month)
    #                 elif placeholder in ['YY', '22']:
    #                     field.clear()
    #                     field.send_keys(year)
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

# from typing import Any
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
#
#
# class PaymentPage:
#     # --- КОНСТАНТЫ СЕЛЕКТОРОВ ---
#     CARD_NUMBER_FIELD = (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")
#     CVC_FIELD = (By.CSS_SELECTOR, "input[placeholder='999']")
#     CVC_FIELD_ANCHOR = (By.CSS_SELECTOR, "input[placeholder='999']")
#     DATE_FIELDS = (By.CSS_SELECTOR, "input[placeholder='MM'], input[placeholder='YY']")
#     SUBMIT_BUTTON = (By.XPATH, ".//button[.//span[text()='Продолжить']]")
#     ERROR_MESSAGE = (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]")
#
#     def __init__(self, driver: Any) -> None:
#         self.driver = driver
#         self.wait = WebDriverWait(self.driver, 20)
#
#     # --- УТИЛИТНЫЙ МЕТОД ДЛЯ ОЖИДАНИЯ ---
#     def _wait_for_element(self, locator: tuple, timeout: int = None) -> WebElement:
#         """
#         Утилитный метод для явного ожидания элемента.
#         Использует self.wait по умолчанию, если таймаут не указан.
#         """
#         wait_to_use = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
#         return wait_to_use.until(
#             EC.visibility_of_element_located(locator),
#             message=f"Элемент не найден или не виден на странице: {locator}"
#         )
#
#     # --- МЕТОДЫ ДЛЯ ВЗАИМОДЕЙСТВИЯ С ФОРМОЙ ---
#
#     def fill_card_number(self, number: str) -> None:
#         """Вводит номер карты."""
#         field = self._wait_for_element(self.CARD_NUMBER_FIELD)
#         field.clear()
#         field.send_keys(number)
#
#     def fill_holder(self, holder: str) -> None:
#         """Вводит имя владельца карты."""
#         cvc_anchor = self._wait_for_element(self.CVC_FIELD_ANCHOR)
#         parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")
#         input_el = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")
#         input_el.clear()
#         input_el.send_keys(holder)
#
#     def fill_cvc(self, cvc: str) -> None:
#         """Вводит CVC/CVV код."""
#         field = self._wait_for_element(self.CVC_FIELD)
#         field.clear()
#         field.send_keys(cvc)
#
#     def fill_date(self, month: str, year: str) -> None:
#         """Вводит срок действия карты (месяц и год)."""
#         # Ждем, пока появятся ВСЕ элементы, найденные по локатору
#         fields = self._wait_for_element(self.DATE_FIELDS)
#         # Примечание: _wait_for_element с presence_of_all_elements_located вернет список
#
#         for field in fields:
#             placeholder = field.get_attribute("placeholder")
#
#             # Проверяем, активен ли элемент (is_enabled), чтобы избежать проблем с readonly полями
#             if field.is_enabled():
#                 if placeholder in ['MM', '08']:
#                     field.clear()
#                     field.send_keys(month)
#                 elif placeholder in ['YY', '22']:
#                     field.clear()
#                     field.send_keys(year)
#
#     def submit(self) -> None:
#         """Отправляет форму оплаты."""
#         btn = self._wait_for_element(self.SUBMIT_BUTTON)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
#         btn.click()
#
#     # --- НОВЫЙ МЕТОД ДЛЯ ПОЛУЧЕНИЯ ТЕКСТА ОШИБКИ ---
#     def get_error_message_text(self) -> str:
#         """
#         Возвращает текст сообщения об ошибке.
#         Инкапсулирует логику поиска и ожидания элемента с ошибкой.
#         """
#         error_element = self._wait_for_element(self.ERROR_MESSAGE)
#         return error_element.text
#

#
# from typing import Any
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
#
# class PaymentPage:
#     def __init__(self, driver: Any) -> None:
#         self.driver = driver
#         # Увеличим таймаут до 20 секунд для надежности
#         self.wait = WebDriverWait(self.driver, 20)
#
#     # --- НОВЫЙ УТИЛИТНЫЙ МЕТОД ДЛЯ ОЖИДАНИЯ ---
#     def _wait_for_element(self, locator: tuple, timeout: int = None) -> WebElement:
#         """
#         Утилитный метод для явного ожидания элемента.
#         Использует self.wait по умолчанию, если таймаут не указан.
#         """
#         # Определяем, какой объект WebDriverWait использовать
#         wait_to_use = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
#
#         return wait_to_use.until(
#             EC.visibility_of_element_located(locator),
#             message=f"Элемент не найден или не виден на странице: {locator}"
#         )
#
#     def fill_card_number(self, number: str) -> None:
#         """Вводит номер карты."""
#         # Используем новый утилитный метод для ожидания
#         field = self._wait_for_element((By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']"))
#         field.clear()
#         field.send_keys(number)
#
#     def fill_holder(self, holder: str) -> None:
#         """Вводит имя владельца карты."""
#         # Оставлен без изменений из-за сложной логики поиска родительского блока.
#         # Можно будет отрефакторить позже с использованием констант-селекторов.
#         cvc_anchor = self.wait.until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']"))
#         )
#         parent_block = cvc_anchor.find_element(
#             By.XPATH, "./ancestor::div[contains(@class, 'form-field')]"
#         )
#         input_el = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")
#         input_el.clear()
#         input_el.send_keys(holder)
#
#     def fill_cvc(self, cvc: str) -> None:
#         """Вводит CVC/CVV код."""
#         # Используем новый утилитный метод для ожидания
#         field = self._wait_for_element((By.CSS_SELECTOR, "input[placeholder='999']"))
#         field.clear()
#         field.send_keys(cvc)
#
#     def fill_date(self, month: str, year: str) -> None:
#         """Вводит срок действия карты (месяц и год)."""
#         # Оставлен без изменений из-за ожидания нескольких элементов (presence_of_all_elements).
#         # Можно будет отрефакторить позже.
#         fields = self.wait.until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[placeholder='08'], input[placeholder='22']"))
#         )
#
#         for field in fields:
#             placeholder = field.get_attribute("placeholder")
#             if placeholder == 'MM' or placeholder == '08':
#                 field.clear()
#                 field.send_keys(month)
#             elif placeholder == 'YY' or placeholder == '22':
#                 field.clear()
#                 field.send_keys(year)
#
#     # def submit(self) -> None:
#     #     """Отправляет форму оплаты."""
#     #     # Используем новый утилитный метод для ожидания кнопки
#     #     btn = self._wait_for_element((By.XPATH, "/html/body/div/div/form/fieldset/div[4]/button"))
#     #
#     #     # Прокручиваем кнопку в видимую область перед кликом
#     #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
#     #     btn.click()
#     #
#     #     # root > div > form > fieldset > div:nth-child(4) > button
#
#     def submit(self) -> None:
#         """Отправляет форму оплаты."""
#         # --- НАДЕЖНЫЙ ЛОКАТОР ПО ТЕКСТУ ВНУТРИ КНОПКИ ---
#         # Ищем кнопку <button>, внутри которой есть <span> с текстом "Продолжить"
#         # Точка в начале ".//" означает поиск на любом уровне вложенности ВНУТРИ элемента <button>
#         btn_locator = (By.XPATH, ".//button[.//span[text()='Продолжить']]")
#
#         # Используем наш утилитный метод для ожидания и поиска элемента
#         btn = self._wait_for_element(btn_locator)
#
#         # Прокручиваем кнопку в видимую область перед кликом
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
#
#         # Выполняем клик
#         btn.click()
