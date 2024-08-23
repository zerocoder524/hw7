from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def get_page_content(browser):
    """Извлекает текст статьи и список ссылок"""
    content = browser.find_element(By.XPATH, "//div[@id='mw-content-text']").text
    links = [link.get_attribute("href") for link in browser.find_elements(By.XPATH, "//div[@id='mw-content-text']//a[@href]")]
    return content, links


def main():
    browser = webdriver.Firefox()
    browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%B0%D0%B0_%D1%81%D1%82%D1%80"
              "%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    assert "Википедия" in browser.title

    while True:
        query = input("Введите ваш запрос: ")
        search_box = browser.find_element(By.ID, "searchInput")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Ждем загрузки страницы

        try:
            # Проверяем, найдена ли статья с таким заголовком
            browser.find_element(By.LINK_TEXT, query)
            print(f"Найдена страница: {query}")
        except NoSuchElementException:
            print(f"Страница с заголовком '{query}' не найдена.")
            continue

        current_content, current_links = get_page_content(browser)
        current_paragraph_index = 0

        while True:
            print("nВыберите действие:")
            print("1. Листать параграфы")
            print("2. Перейти на связанную страницу")
            print("3. Выйти")

            choice = input("Введите номер действия: ")

            if choice == "1":
                print("n--- Текст статьи ---")
                paragraphs = current_content.split('nn')
                if current_paragraph_index < len(paragraphs):
                    print(paragraphs[current_paragraph_index])
                    current_paragraph_index += 1
                else:
                    print("Больше параграфов нет.")

            elif choice == "2":
                print("n--- Доступные ссылки ---")
                for i, link in enumerate(current_links):
                    print(f"{i+1}. {link}")

                link_choice = input("Введите номер ссылки: ")
                if link_choice.isdigit() and int(link_choice) in range(1, len(current_links) + 1):
                    browser.get(current_links[int(link_choice) - 1])
                    time.sleep(2)  # Ждем загрузки страницы
                    current_content, current_links = get_page_content(browser)
                    current_paragraph_index = 0
                    print(f"nПереход на страницу: {browser.title}")
                    print(f"--- Текст статьи ---n{current_content.split('nn')[0]}")
                else:
                    print("Неверный выбор.")

            elif choice == "3":
                print("До свидания!")
                browser.quit()
                break

            else:
                print("Неверный выбор.")

if __name__ == "__main__":
    main()
