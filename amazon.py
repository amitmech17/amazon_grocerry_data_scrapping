from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json


chrome_options = Options()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
data = {}
driver.implicitly_wait(10)
driver.get("https://www.amazon.in/b?node=21246959031&pf_rd_r=8JK44VGQD09RNN5BQS2R&pf_rd_p=ed208a6a-6572-4ef5-8e0e-3106ec5eb1bf")

categoty = driver.find_elements_by_xpath("//h4[@class='a-size-small a-spacing-top-mini a-color-base a-text-bold']")
category_list = []
for cat in categoty:
    category_list.append(cat.text)
# print((category_list))
del category_list[0:2]
print(category_list)
for i in category_list:
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(
        "https://www.amazon.in/b?node=21246959031&pf_rd_r=8JK44VGQD09RNN5BQS2R&pf_rd_p=ed208a6a-6572-4ef5-8e0e-3106ec5eb1bf")
    time.sleep(2)
    # driver.find_element_by_xpath("//h4[contains(text(),'{}')]".format(i)).location_once_scrolled_into_view
    driver.find_element_by_xpath("//h4[text()='{}']".format(i)).click()
    z = {}
    data[i] = z
    sub_categories = driver.find_elements_by_xpath("//li[@class='a-spacing-micro s-navigation-indent-2']")
    sub_cat = []
    for ginger in sub_categories:
        sub_cat.append(ginger.text)
    # del sub_cat[0:2]
    # print((sub_cat))
    for sub_category in sub_cat:
        # print(sub_category)
        # driver.find_element_by_xpath("//span[contains(text(),'{}')]".format(sub_category)).location_once_scrolled_into_view
        driver.find_element_by_xpath(".//span[text()='{}']".format(sub_category)).click()
        z[sub_category] = {}
        time.sleep(2)
        sub_cat_item = driver.find_elements_by_xpath("//li[@class='a-spacing-micro s-navigation-indent-2']//span["
                                                     "@class='a-size-base a-color-base']")
        sub_cat_items = []
        for lip in sub_cat_item:
            if "'" in lip.text:
                lip = lip.text.split("'")[0]
                sub_cat_items.append(lip)
            else:
                sub_cat_items.append(lip.text)
        # del sub_cat_items[0:5]
        # print(sub_cat_items)
        time.sleep(3)
        for item in sub_cat_items:
            print(item)
            if item == "Baking Supplies" or item == "Cooking Pastes & Sauces" or item == "Coconut Water" or item == "Coffee & Espresso" or item == "Cola & Soft Drinks" or item == "Concentrated Syrups & Squash":
                continue
            cat_item_text = item
            time.sleep(5)
            driver.find_element_by_xpath(".//span[text()='{}']".format(item)).click()
            z[sub_category][cat_item_text] = []
            while True:
                time.sleep(2)
                all_item = driver.find_elements_by_xpath(".//div[@class='a-section a-spacing-medium']")
                for li in all_item:
                    u = {}
                    # print(li.find_element_by_xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']").text)
                    u["product_name"] = (
                        li.find_element_by_xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']").text)
                    u["product_image_list"] = (li.find_element_by_xpath(".//img[@class='s-image']").get_attribute("src"))
                    actual_price = len(li.find_elements_by_xpath(".//span[@class='a-price']")) > 0
                    if actual_price is False:
                        u["product_actual_price"] = None
                    else:
                        u["product_actual_price"] = li.find_element_by_xpath(".//span[@class='a-price']").text
                    discounted_price = len(li.find_elements_by_xpath(".//span[@class='a-price a-text-price']/span[1]")) > 0
                    if discounted_price is False:
                        u["product_discounted_price"] = None
                    else:
                        u["product_discounted_price"] = li.find_element_by_xpath(".//span[@class='a-price a-text-price']/span[1]").text
                    z[sub_category][cat_item_text].append(u)
                try:
                    driver.find_element_by_xpath("//a[contains(text(),'Next')]").location_once_scrolled_into_view
                    driver.execute_script("window.scrollTo(-50, 0);")
                    time.sleep(1)
                    driver.find_element_by_xpath("//a[contains(text(),'Next')]").click()
                except:
                    break
            print(json.dumps(data))
            driver.find_element_by_xpath("(//span[@class='s-back-arrow aok-inline-block'])[2]").location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(-100, 0);")
            time.sleep(2)
            driver.find_element_by_xpath("(//span[@class='s-back-arrow aok-inline-block'])[2]").click()
        driver.find_element_by_xpath("//span[@class='s-back-arrow aok-inline-block']").click()
    print(json.dumps(data))


