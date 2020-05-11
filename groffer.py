from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json

options = Options()
options.add_argument("window-size=1080,720")
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get("https://grofers.com/cn/grocery-staples/cid/16")
time.sleep(10)
driver.find_element_by_xpath("//div[contains(text(),'Mumbai')]").click()
data = {}
time.sleep(10)
driver.implicitly_wait(20)
categories = driver.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]/div[1]/div["
                                           "1]/div[1]/div[2]/nav[1]/li")
for category in categories:
    if "more" in category.get_attribute("textContent"):
        break
    else:
        # or category.get_attribute("textContent") == "Grocery & Staples"
        cat_list = ["test"]
        if category.get_attribute("textContent") in cat_list:
            continue
        category.click()
        time.sleep(5)
        # print(category.get_attribute("textContent"))
        category = category.get_attribute("textContent")
        z = {}
        data[category] = z
        sub_categories = driver.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]/div["
                                                       "2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/nav[1]/li")
        i = 0
        for sub_cat in sub_categories:
            if i == 0:
                # print("in this zero")
                i = i + 1
                continue
            else:
                sub_cat_text = sub_cat.get_attribute("textContent")
                print(sub_cat_text)
                sub_cat_list = ["test"]
                # sub_cat_list = ["Chips & Crisps","Atta & Other Flours","Personal Care Best offers","Buy 1 Get 1 Free","Household Best Offers","Best Offers"]
                if sub_cat_text in sub_cat_list:
                    continue
                sub_cat.location_once_scrolled_into_view
                sub_cat.click()
                time.sleep(5)
                z[sub_cat_text] = {}
                sub_cat_item = driver.find_elements_by_xpath("//ul[@class='category-sub-list list-unstyled show-el']//li")

                # print("came here")

                for item in sub_cat_item:
                    cat_item_text = item.get_attribute("textContent")
                    pro_list = ["Sunflower Oils","Antiseptics","Toilet Cleaners","Mustard Oils"]
                    if cat_item_text in pro_list:
                        continue
                    # print("cart_item")
                    item.location_once_scrolled_into_view
                    item.click()
                    time.sleep(5)
                    z[sub_cat_text][cat_item_text] = []
                    all_item = driver.find_elements_by_xpath("//a[@class='product__wrapper']")
                    op = 1
                    for li in all_item:
                        u = {}
                        item.location_once_scrolled_into_view
                        li.click()
                        time.sleep(5)
                        u["product_name"] = (
                            li.find_element_by_xpath("//h1[@class='pdp-product__name']").get_attribute("textContent"))
                        u["product_quantity"] = (
                            li.find_element_by_xpath("//div[@class='product-variant__list']").get_attribute(
                                "textContent"))
                        images_list = driver.find_elements_by_xpath("//div[@class='pdp-product__container']//div[1]//div[1]//div[1]//div[1]//div[1]//img")
                        image_list = ""
                        for image in images_list:
                            if image.get_attribute("src") is not None:
                                image_list = image_list + image.get_attribute("src") + ","
                        u["product_iamge_list"] = image_list
                        try:
                            u["product_actual_price"] = (
                                li.find_element_by_xpath(
                                    "//div[@class='pdp-product__old-price']").get_attribute(
                                    "textContent"))
                            u["product_discounted_price"] = (
                                li.find_element_by_xpath("//div[@class='pdp-product__new-price']").get_attribute(
                                    "textContent"))
                        except:
                            u["product_actual_price"] = (
                                li.find_element_by_xpath(
                                    "//span[@class='pdp-product__price--new pdp-product__price--black']").get_attribute(
                                    "textContent"))
                            u["product_discounted_price"] = None
                        # print(u)
                        driver.back()
                        time.sleep(5)
                        z[sub_cat_text][cat_item_text].append(u)
                        op += 1
                        # print(json.dumps(z))
            print("final category json")
            print(json.dumps(data))
            i = i + 1
