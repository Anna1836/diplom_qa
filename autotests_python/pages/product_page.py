from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    """
    Класс-описание страницы товара.
    Инкапсулирует локаторы и методы для выбора способа покупки.
    """
    # Локатор для кнопки "Купить в кредит"
    CREDIT_BUY_BUTTON = (By.XPATH, "//span[contains(text(), 'в кредит')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def _find_element(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент не найден или не кликабелен: {locator}"
        )

    def buy_in_credit(self) -> PaymentPage:
        """
        Нажимает кнопку 'Купить в кредит' и возвращает объект страницы оплаты.
        :return: Экземпляр PaymentPage
        """
        credit_btn = self._find_element(self.CREDIT_BUY_BUTTON)
        credit_btn.click()

        # После нажатия мы попадаем на страницу оплаты, создаем её объект
        payment_page = PaymentPage(self.driver)
        # И открываем её (если метод open() нужен для финализации перехода)
        payment_page.open()
        return payment_page