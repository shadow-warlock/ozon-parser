from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


def load(url):
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    item_name = driver.find_element_by_css_selector('[data-widget="webProductHeading"]>h1').text
    item_score = driver.find_element_by_css_selector(
        '[data-widget="container"] [data-widget="reviewProductScore"]>div>div>div>div').get_attribute('style').replace(
        "width: ", "").replace(";", '')
    item_price = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/span[1]').text.replace(
        ' ', '')

    print("Name:" + item_name + " Price:" + item_price + " Score:" + item_score)
    return driver


driver = load("https://www.ozon.ru/context/detail/id/159397500/")
recommends = driver.find_elements_by_css_selector('[data-widget="skuShelfCompare"]>div>div>div>div>div>div>a')
print("---RECOMMENDS---")
for element in recommends:
    load(element.get_property("href"))

sponsored = driver.find_elements_by_css_selector('[data-widget="skuShelfGoods"]>div>div>div>div>div>a')
print("---SPONSORED---")
for element in sponsored:
    load(element.get_property("href"))

driver.close()
