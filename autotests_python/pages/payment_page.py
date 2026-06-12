

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


