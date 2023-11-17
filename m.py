import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# def time_of_function(function):
#     def wrapped(*args):
#         start_time = time.perf_counter_ns()
#         res = function(*args)
#         print(time.perf_counter_ns() - start_time)
#         return res
#
#     return wrapped
#
#
# @time_of_function
def get(url, count, min_price, max_price):
    if min_price != 0 and max_price != 0:
        url = url + f'#?filters=%7B"88C83F68482F447C9F4E401955196697"%3A%7B"' \
                    f'min"%3A{min_price}%2C"max"%3A{max_price}%7D%7D'
    elif max_price != 0:
        url = url + f'#?filters=%7B"88C83F68482F447C9F4E401955196697"%3A%7B"max"%3A{max_price}%7D%7D'
    elif min_price != 0:
        url = url + f'#?filters=%7B"88C83F68482F447C9F4E401955196697"%3A%7B"max"%3A{min_price}%7D%7D'

    s = Service(r'C:\Users\7887346\PycharmProjects\megamarket\chromedriver\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    wait = WebDriverWait(driver, timeout=10)
    #driver.maximize_window()
    results = []
    try:
        driver.get(url)
        try:
            time.sleep(2)
            button = driver.find_element(By.CLASS_NAME, 'btn')  # город
            wait.until(lambda d: button.is_displayed())
            button.click()
            button = driver.find_element(By.CLASS_NAME, 'close-button')  # рекламный баннер
            wait.until(lambda d: button.is_displayed())
            button.click()
        except Exception as ex:
            print(ex)
        for i in range(count):
            try:
                time.sleep(2.1)
                button = driver.find_element(By.CLASS_NAME, 'btn-cloudy')
            except Exception:
                print('Страницы закончились')
                break
            try:
                wait.until(lambda d: button.is_displayed())
                button.click()
            except Exception as ex:
                print(ex)
                break
    except Exception as ex:
        print(ex)
    finally:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        driver.quit()
        items = soup.findAll('div', class_="item-info")
        for item in items:
            result = {}
            try:
                result['name'] = item.find('a', class_="ddl_product_link").text.strip().replace('\n', '')
            except Exception:
                continue
            try:
                result['price'] = item.find('div', class_='item-price').text.replace('\xa0₽', '').replace(' ', '')
            except Exception:
                continue
            try:
                result['bonus'] = item.find('span', class_="bonus-amount").text.replace(' ', '')
            except Exception:
                result['bonus'] = 0
            try:
                result['url'] = 'https://megamarket.ru' + item.find('a', class_="ddl_product_link").get("href")
            except Exception:
                continue
            if result not in results:
                results.append(result)
        return results


def main():
    res = []

    categories = [
        {'url': 'https://megamarket.ru/catalog/smartfony/',  # ссылка на категорию
         'pages': 10,  # количество страниц, ~40 товаров на одной
         # ставьте 0, если не хотите менять
         'min_price': 0,  # минимальная цена
         'max_price': 0  # максимальная цена (без учета кэшбека)
         },
        {'url': 'https://megamarket.ru/catalog/televizory/',  # ссылка на категорию
         'pages': 10,  # количество страниц, ~40 товаров на одной
         # ставьте 0, если не хотите менять
         'min_price': 0,  # минимальная цена
         'max_price': 0  # максимальная цена (без учета кэшбека)
         },
    ]

    for category in categories:
        res.append(get(category['url'], category['pages'], category['min_price'], category['max_price']))

    with open("f.json", "w") as f:
        json.dump(res, f)


if __name__ == '__main__':
    main()
