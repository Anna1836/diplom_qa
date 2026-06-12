# # from selenium.webdriver.remote.webelement import WebElement
# # from selenium.webdriver.support.wait import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.by import By
# #
# #
# # class PaymentPage:
# #     def __init__(self, driver):
# #         self.driver = driver
# #         self.wait = WebDriverWait(self.driver, 20)
# #
# #     def fill_card_number(self, number: str):
# #         field = self.wait.until(
# #             EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"))
# #         )
# #         field.clear()
# #         field.send_keys(number)
# #
# #     def fill_holder(self, holder: str):
# #         anchor = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
# #         block = anchor.find_element(By.XPATH, "./ancestor::*[contains(@class, 'form-field')]")
# #         input = block.find_element(By.CSS_SELECTOR, "input.input__control")
# #         input.clear()
# #         input.send_keys(holder)
# #
# #     # Остальные методы заполнения полей (month, year, cvc) аналогичны.
# #
# #     def submit(self):
# #         button = self.wait.until(
# #             EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/form/fieldset/div[4]/button"))
# #         )
# #         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
# #         button.click()
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
#         self.wait = WebDriverWait(self.driver, 15)
#
#     def fill_card_number(self, number: str) -> None:
#         """Номер карты"""
#         field = self.wait.until(
#             EC.element_to_be_clickable(
#                 (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")
#             )
#         )
#         field.clear()
#         field.send_keys(number)
#
#     def fill_holder(self, holder: str) -> None:
#         """Имя владельца"""
#         # Берём за точку привязки поле CVV
#         cvc_anchor = self.wait.until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']"))
#         )
#         # Поднимаемся вверх к общему контейнеру
#         parent_block = cvc_anchor.find_element(
#             By.XPATH, "./ancestor::div[contains(@class, 'form-field')]"
#         )
#         # Внутри этого блока находим поле имени
#         input_el = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")
#         input_el.clear()
#         input_el.send_keys(holder)
#
#     def fill_cvc(self, cvc: str) -> None:
#         """CVV/CVC"""
#         field = self.wait.until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']"))
#         )
#         field.clear()
#         field.send_keys(cvc)
#
#     def fill_date(self, month: str, year: str) -> None:
#         """Срок действия"""
#         self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))
#         ).clear()
#         self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))
#         ).send_keys(month)
#
#         self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))
#         ).clear()
#         self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))
#         ).send_keys(year)
#
#     def submit(self) -> None:
#         """Отправка формы"""
#         btn = self.wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "/html/body/div/div/form/fieldset/div[4]/button")
#             )
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
#         btn.click()
#
# # Вводим CVC/CVV код
# parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")
# # --- 2. Заполнение даты действия карты ---
# # Месяц и год обычно находятся вне родительского блока CVC, поэтому ищем их отдельно.
# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08") # Месяц
# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26") # Год

from typing import Any
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class PaymentPage:
    def __init__(self, driver: Any) -> None:
        self.driver = driver
        # Увеличим таймаут до 20 секунд для надежности
        self.wait = WebDriverWait(self.driver, 20)

    def fill_card_number(self, number: str) -> None:
        """Вводит номер карты."""
        field = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")
            )
        )
        field.clear()
        field.send_keys(number)

    def fill_holder(self, holder: str) -> None:
        """Вводит имя владельца карты."""
        cvc_anchor = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']"))
        )
        parent_block = cvc_anchor.find_element(
            By.XPATH, "./ancestor::div[contains(@class, 'form-field')]"
        )
        input_el = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")
        input_el.clear()
        input_el.send_keys(holder)

    def fill_cvc(self, cvc: str) -> None:
        """Вводит CVC/CVV код."""
        # Используем element_to_be_clickable вместо visibility_of...
        field = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='999']"))
        )
        field.clear()
        field.send_keys(cvc)

    def fill_date(self, month: str, year: str) -> None:
        """Вводит срок действия карты (месяц и год)."""
        # Находим оба поля один раз, чтобы избежать двойного ожидания
        fields = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[placeholder='08'], input[placeholder='22']"))
        )

        for field in fields:
            placeholder = field.get_attribute("placeholder")
            if placeholder == 'MM' or placeholder == '08':
                field.clear()
                field.send_keys(month)
            elif placeholder == 'YY' or placeholder == '22':
                field.clear()
                field.send_keys(year)


    def submit(self) -> None:
        """Отправляет форму оплаты."""
        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/form/fieldset/div[4]/button")
            )
        )
        # Прокручиваем кнопку в видимую область перед кликом
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()


# # В файле autotests_python/pages/payment_page.py
#
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# class PaymentPage:
#     # ... другие методы __init__, fill_*, submit() ...
#
#     def get_success_notification(self):
#         """Ищет глобальное уведомление об успешной оплате."""
#         return self.wait.until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, ".notification__content.success"))
#         )
#
#     def get_error_message_by_text(self, error_text):
#         """
#         Ищет текст ошибки в любом месте формы.
#         Это более надежный способ, чем поиск по соседним элементам.
#
#         :param error_text: Текст ошибки, который нужно найти.
#         """
#         locator = (By.XPATH,
#                    f"//*[contains(@class, 'input') or contains(@class, 'field')]//span[contains(text(), '{error_text}')]")
#         return self.wait.until(EC.visibility_of_element_located(locator))