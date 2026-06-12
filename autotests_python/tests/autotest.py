# from selenium import webdriver
# import unittest
#
#
# class SimpleSeleniumTest(unittest.TestCase):
#
#     def setUp(self):
#         # Запускаем браузер Chrome
#         self.driver = webdriver.Chrome()
#
#     def test_google_title(self):
#         driver = self.driver
#
#         # Открываем главную страницу Google
#         driver.get("https://www.google.com")
#
#         # Проверяем, соответствует ли заголовок страницы ожидаемому значению
#         expected_title = 'Google'
#         actual_title = driver.title
#         self.assertEqual(expected_title, actual_title)

#     def tearDown(self):
#         # Закрываем браузер после завершения теста
#         self.driver.quit()
#
#
# if __name__ == "__main__":
#     unittest.main()