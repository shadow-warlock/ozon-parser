import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from test import parse

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
for i in range(1, 20):
    if i == 2:
        i = 3
    driver.get("https://www.ozon.ru/category/televizory-15528/?page=" + str(i))
    driver.implicitly_wait(3)  # seconds
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    recommends = driver.find_elements_by_css_selector(
        'html body div#__nuxt div.layout-page.desktop div.block-vertical div.container.c0x2 div.c1d div.c0u9 div.ce4.c0v0 div div.widget-search-result-container.ap div.ap0>div')
    for element in recommends:
        url = element.find_element_by_xpath("div/div/div[1]/a").get_attribute("href")
        parse(url)

driver.close()
