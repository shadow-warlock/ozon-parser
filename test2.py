import sqlite3
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from test import parse, get_id

connect = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM


options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
flag = False
for i in range(1, 21):
    if i == 2:
        i = 3
    driver.get("https://www.ozon.ru/category/televizory-15528/?page=" + str(i))
    driver.implicitly_wait(3)  # seconds
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elements = driver.find_elements_by_css_selector(
        'html body div#__nuxt div.layout-page.desktop div.block-vertical div.container.c0x2 div.c1d div.c0u9 div.ce4.c0v0 div div.widget-search-result-container.ap div.ap0>div')
    for j in range(0, len(elements)):
        element = elements[j]
        url = element.find_element_by_xpath("div/div/div[1]/a").get_attribute("href")
        id = get_id(url)
        if id == "149329627":
            flag = True
        if not flag:
            print(id + " skip")
            continue
        print(url)
        parse(url, "v1")

driver.close()
