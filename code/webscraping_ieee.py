import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from time import sleep

# Read search strings
lit_strings = []
with open("data/search_strings_ieee.csv", "r+", newline="") as csvf:
    reader = csv.reader(csvf, delimiter=",")
    writer = csv.writer(csvf)
    driver = webdriver.Firefox()
    for row in reader:
        if row != []:
            # delete prefix for IEEE
            search_string = row[0]
            # Find the index of the first opening parenthesis
            # index_of_open_parenthesis = search_string.find("(")
            # search_string = search_string[index_of_open_parenthesis:]

            # set search parameters
            driver.get("https://ieeexplore.ieee.org")
            sleep(2)
            select_ele = driver.find_element(
                By.XPATH, "/html/body/div[5]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[1]/label/select")
            all_options = select_ele.find_elements(By.TAG_NAME, "option")
            for option in all_options:
                if option.text == "Journals & Magazines":
                    option.click()
                    break
            sleep(1)

            # apply search strings
            # search_bar = driver.find_element(
            #     By.XPATH, "/html/body/div[5]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/input")
            search_form = driver.find_element(
                By.TAG_NAME, "form")
            search_bar = search_form.find_elements(By.TAG_NAME, "input")[0]
            # search_bar = driver.find_element(
            # By.CSS_SELECTOR, "input.search-by ng-pristine ng-valid ng-touched")
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)
            # sleep(10)

            # Read
            # Read only jounals and early access papers
            start_time = time.time()
            results = None
            while time.time() <= start_time + 6:
                try:
                    results = driver.find_element(
                        By.XPATH, "/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[1]/div[2]/xpl-search-dashboard/section/div/h1")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            with open("data/search_results_ieee.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((search_string, "0"))
                else:
                    position = results.text.find("of")
                    if position == -1:
                        hits = 0
                    else:
                        hits = results.text[position:].split()[1]
                    writer.writerow((search_string, hits))

    driver.close()
