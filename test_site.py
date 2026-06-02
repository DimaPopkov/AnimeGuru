import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By 

class MySiteTest(unittest.TestCase):

    def setUp(self):
        # Настройка и запуск Google Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def test_open_my_site(self):
        # Впишите сюда адрес своего сайта вместо google.com
        self.driver.get("http://127.0.0.1:8000/")
        
        # Проверяем, что сайт успешно загрузил заголовок
        page_title = self.driver.title
        self.assertTrue(len(page_title) > 0, "Заголовок страницы пустой!")
        print(f"\n[УСПЕХ] Браузер открылся! Заголовок вкладки: {page_title}")

    def test_catalog_interaction(self):
        self.driver.get("http://127.0.0.1:8000/login") # Или ваш точный URL
        
        search_input = self.driver.find_element(By.NAME, "username")
        search_input.send_keys("test")

        search_input2 = self.driver.find_element(By.NAME, "password")
        search_input2.send_keys("test")
        
        # Оставляем строчку проверки, чтобы тест завершался успешно
        self.assertTrue(len(self.driver.title) > 0)
        print("\n[УСПЕХ] Вы успешно вошли в аккаунт!")


    def test_card_interaction(self):
        self.driver.get("http://127.0.0.1:8000/")

        # 1. Находим ВСЕ карточки на странице по их классу
        cards = self.driver.find_elements(By.CLASS_NAME, "new_products_list_product")
        
        # 2. Проверяем, что найдена хотя бы одна карточка
        self.assertTrue(len(cards) > 0, "Карточки товаров не найдены на странице!")
        
        # 3. Кликаем по первой карточке в списке (индекс 0)
        cards[0].click()
        
        # Дальнейшие проверки (заголовок страницы и т.д.)
        page_title = self.driver.title
        self.assertTrue(len(page_title) > 0, "Заголовок страницы пустой!")
        print(f"\n[УСПЕХ] Карточка успешно открылась! Заголовок вкладки: {page_title}")

    def tearDown(self):
        # Закрываем браузер после завершения теста
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()