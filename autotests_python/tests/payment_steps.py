# В этом файле мы описываем не элементы страницы, а действия пользователя.

class PaymentSteps:
    """
    Класс, инкапсулирующий шаги пользователя на странице оплаты.
    """

    def __init__(self, payment_page):
        """
        :param payment_page: Экземпляр класса PaymentPage, с которым мы будем работать.
        """
        self.page = payment_page

    def pay_with_card(self, card_data: dict):
        """
        Выполняет полный цикл оплаты картой.
        :param card_data: Словарь с данными карты (номер, владелец, cvc, месяц, год).
        """
        # Используем уже готовые методы из PaymentPage
        self.page.fill_card_number(card_data["number"])
        self.page.fill_holder(card_data["holder"])
        self.page.fill_cvc(card_data["cvc"])
        self.page.fill_date(card_data["month"], card_data["year"])

        # Отправляем форму
        self.page.submit()