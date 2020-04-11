from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get("https://www.ozon.ru/context/detail/id/159397500/")
driver.implicitly_wait(5)  # seconds
item_name = driver.find_element_by_css_selector('[data-widget="webProductHeading"]>h1').text
print(item_name)
item_score = driver.find_element_by_css_selector(
    '[data-widget="container"] [data-widget="reviewProductScore"]>div>div>div>div').get_attribute('style').replace(
    "width: ", "").replace(";", '')
print(item_score)
item_price = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/span[1]').text
print(item_price)

# recommendElDiv = driver.find_element_by_css_selector('[data-widget="skuShelfCompare"]')
# actions = ActionChains(driver)
# actions.move_to_element(recommendElDiv)
# actions.perform()

recommends = driver.find_elements_by_css_selector(
    '[data-widget="skuShelfCompare"]>div>div>div>div>div>div>a>div:nth-child(2)')

button = driver.find_elements_by_css_selector('[qa-id="slider-next"]>button')[1]
# button.click()
# button.click()
# button.click()
# button.click()
# button.click()
# button.click()

for element in recommends:
    name = element.find_element_by_css_selector('div:nth-child(3)').get_property("textContent").strip()
    score = element.find_element_by_css_selector('div:nth-child(4)').get_attribute('title')
    price = element.find_element_by_css_selector('div:nth-child(2)>div:nth-child(1)>span>span>span').get_property(
        "textContent").strip()
    print(name + " " + price + " " + score)

driver.get_screenshot_as_file("screen.png")
driver.close()
