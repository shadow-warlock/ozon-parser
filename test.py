from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


def load(url):
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.implicitly_wait(20)  # seconds
    driver.execute_script("window.scrollTo(0, 300);")
    id = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[4]/div[1]/div/div[1]/span").text.split(": ")[1]
    driver.save_screenshot("screens/"+id+".png")
    item_name = driver.find_element_by_css_selector('[data-widget="webProductHeading"]>h1').text
    item_sale = driver.find_elements_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[1]/div[1]/span[1]')
    if len(item_sale) != 0:
        item_sale = item_sale[0].text
    else:
        item_sale = "-"
    item_score = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/div').get_attribute('title')
    item_price = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/span[1]').text.replace(
        ' ', '')
    item_salary_name = driver.find_elements_by_xpath(
        "/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div/div/span")
    reviews = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[1]/div[4]/div[2]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/a").text
    reviews = reviews.split()[0]
    salary_all_count = "-"
    salary_today_count = "-"
    if len(item_salary_name) != 0:
        name = item_salary_name[0].text
        if "Купили более" in name:
            salary_all_count = name.split()[2]
        elif "за сегодня" in name and "покуп" in name:
            salary_today_count = name.split()[0]
    print(
        "ID:" + id + " Name:" + item_name + " Price:" + item_price + " Score:" + item_score + " Sale:" + item_sale + " salary all count:" + salary_all_count + " salary today count:" + salary_today_count + " Reviews:" + reviews)
    return driver


def parse(url):
    print("---MAIN---")
    driver = load(url)
    recommends = driver.find_elements_by_css_selector('[data-widget="skuShelfCompare"]>div>div>div>div>div>div>a')
    print("---RECOMMENDS---")
    for element in recommends:
        local_driver = load(element.get_property("href").split("?")[0])
        local_driver.close()

    sponsored = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[5]/div/div[2]/div/div[3]').find_elements_by_css_selector(
        "div>div>div>div>div>a")
    print("---SPONSORED---")
    for element in sponsored:
        local_driver = load(element.get_property("href").split("?")[0])
        local_driver.close()

    driver.set_window_size(1366, 5000)  # because firefox not scroll to element
    also_bayed = driver.find_elements_by_css_selector(
        "#__nuxt>div>div.block-vertical>div:nth-child(6)>div>div:nth-child(2)>div>div:nth-child(4) a")
    print("---ALSO BAYED---")
    for element in also_bayed:
        local_driver = load(element.get_property("href").split("?")[0])
        local_driver.close()

    driver.close()
