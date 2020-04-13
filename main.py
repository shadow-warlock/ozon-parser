import csv
import re
import sqlite3
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.native_events_enabled = False
drivers = []

wait_time = 10


def load(url, type):
    id = get_id(url)
    print(id)
    connect = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM
    data = connect.cursor().execute("""SELECT * FROM items WHERE id=?""", [id]).fetchall()
    connect.close()
    if len(data) > 0:
        print(id + " load from db")
        return data[0][1] + "," + type
    # id = driver.find_element_by_css_selector("[data-widget=detailSKU]").text.split(": ")[1]
    driver = webdriver.Firefox(options=options)
    drivers.append(driver)
    driver.implicitly_wait(wait_time)  # seconds
    driver.get(url)
    item_name = driver.find_elements_by_css_selector('[data-widget="webProductHeading"]>h1')
    if len(item_name) == 0:
        return None
    item_name = item_name[0].text
    item_sale = driver.find_elements_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[1]/div[1]/span[1]')
    if len(item_sale) != 0:
        item_sale = item_sale[0].text
    else:
        item_sale = "-"
    item_score = driver.find_elements_by_css_selector('[data-widget="reviewProductScore"] div[title]')
    if len(item_score) == 0:
        item_score = "-"
    else:
        item_score = item_score[0].get_attribute('title')
    item_price = driver.find_elements_by_css_selector('[data-widget="webSale"]>div>div>div>div>div>span')
    if len(item_price) > 0:
        item_price = item_price[0].text.replace(' ', '')
    else:
        item_price = "-"
    item_salary_name = driver.find_elements_by_xpath(
        "/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div/div/span")
    if len(item_salary_name) != 0:
        name = item_salary_name[0].text
        current_sleep = 0
        while name == "":
            current_sleep += 1
            if current_sleep > 2:
                break
            print("nameWhile")
            time.sleep(1)
            item_salary_name = driver.find_elements_by_xpath(
                "/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div/div/span")
            if len(item_salary_name) == 0:
                break
            name = item_salary_name[0].text
    reviews = driver.find_elements_by_css_selector('[data-widget="reviewProductScore"] a')
    if len(reviews) != 0:
        reviews = reviews[0].get_property("textContent").split()[0]
    else:
        reviews = "0"
    salary_all_count = "-"
    salary_today_count = "-"
    salary_week_count = "-"
    if len(item_salary_name) != 0:
        name = item_salary_name[0].text
        if "Купили более" in name:
            salary_all_count = name.split()[2]
        elif "за сегодня" in name and "покуп" in name:
            salary_today_count = name.split()[0]
        elif "за неделю" in name and "покуп" in name:
            salary_week_count = name.split()[0]
    print(
        "ID:" + id + " Name:" + item_name + " Price:" + item_price + " Score:" + item_score + " Sale:" + item_sale + " salary all count:" + salary_all_count + " salary today count:" + salary_today_count + " salary week count:" + salary_week_count + " Reviews:" + reviews)
    driver.close()
    drivers.remove(driver)
    data = ",".join(
        [id, item_name, item_price, item_score, item_sale, salary_all_count, salary_today_count, salary_week_count,
         reviews])
    connect = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM
    connect.cursor().execute("""INSERT INTO items VALUES (?,?)""", [id, data])
    connect.commit()
    connect.close()
    return data + "," + type


def parse(url, pack, reload=0):
    print("---MAIN---")
    driver = webdriver.Firefox(options=options)
    drivers.append(driver)
    driver.set_window_size(1366, 9000)  # because firefox not scroll to element
    driver.implicitly_wait(wait_time)  # seconds
    driver.get(url)
    main_data = load(url, "main")
    if main_data is None:
        return

    print("---RECOMMENDS---")
    recommends = driver.find_elements_by_css_selector('[data-widget="skuShelfCompare"]>div>div>div>div>div>div>a')
    current_sleep = 0
    while len(recommends) == 0:
        current_sleep += 1
        if current_sleep > 2:
            if reload > 1:
                break
            driver.close()
            drivers.remove(driver)
            parse(url, pack, reload+1)
            return
        time.sleep(1)
        print("recWhile")
    recommends_data = []
    for element in recommends:
        recommends_temp_data = load(element.get_property("href").split("?")[0], "recommends")
        recommends_data.append(recommends_temp_data)

    print("---SPONSORED---")
    sponsored = driver.find_elements_by_css_selector('[data-widget="skuShelfGoods"][title="Спонсорские товары"] a')
    current_sleep = 0
    while len(sponsored) == 0:
        current_sleep += 1
        if current_sleep > 2:
            if reload > 1:
                break
            driver.close()
            drivers.remove(driver)
            parse(url, pack, reload+1)
            return
        driver.save_screenshot("sponsored_screen.png")
        print("sponsoredWhile")
        time.sleep(1)
        sponsored = driver.find_elements_by_css_selector('[data-widget="skuShelfGoods"][title="Спонсорские товары"] a')
    sponsored_data = []
    for element in sponsored:
        sponsored_temp_data = load(element.get_property("href").split("?")[0], "sponsored")
        sponsored_data.append(sponsored_temp_data)

    print("---ALSO-BUYED---")
    also_buyed = driver.find_elements_by_css_selector(
        "#__nuxt>div>div.block-vertical>div:nth-child(6)>div>div:nth-child(2)>div>div:nth-child(4) a")
    also_buyed_data = []
    for element in also_buyed:
        also_buyed_data_temp = load(element.get_property("href").split("?")[0], "also_buy")
        also_buyed_data.append(also_buyed_data_temp)

    driver.close()
    drivers.remove(driver)
    with open('data/data' + pack + '.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([main_data] + recommends_data + sponsored_data + also_buyed_data)
        csvfile.close()


def get_id(url):
    return list(filter(lambda e: e != '', re.split(r'[\-/]', url)))[-1]


# parse("https://www.ozon.ru/context/detail/id/154925584/", "test")
