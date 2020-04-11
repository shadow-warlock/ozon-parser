from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


def load(url):
    print(url)
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.implicitly_wait(10)  # seconds
    item_name = driver.find_element_by_css_selector('[data-widget="webProductHeading"]>h1').text
    item_sale = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[1]/div[1]/span[1]').text
    item_score = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/div').get_attribute('title')
    item_price = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/span[1]').text.replace(
        ' ', '')
    item_100 = driver.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div/div/span/span")
    reviews = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/a").text
    reviews = reviews.split()[0]
    if len(item_100) != 0:
        item_100 = "True"
    else:
        item_100 = "False"
    print("Name:" + item_name + " Price:" + item_price + " Score:" + item_score + " Sale:" + item_sale + " 100+:" + item_100 + " Reviews:" + reviews)
    return driver


driver = load("https://www.ozon.ru/context/detail/id/159397500/")
recommends = driver.find_elements_by_css_selector('[data-widget="skuShelfCompare"]>div>div>div>div>div>div>a')
print("---RECOMMENDS---")
for element in recommends:
    local_driver = load(element.get_property("href").split("?")[0])
    local_driver.close()

sponsored = driver.find_elements_by_css_selector('[data-widget="skuShelfGoods"]>div>div>div>div>div>a')
print("---SPONSORED---")
for element in sponsored:
    local_driver = load(element.get_property("href").split("?")[0])
    local_driver.close()

driver.close()
