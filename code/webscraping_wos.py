import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from time import sleep

# Read search strings
is_title = True
with open("data/search_strings.csv", "r+", newline="") as csvf:
    reader = csv.reader(csvf, delimiter=",")
    driver = webdriver.Firefox()
    for row in reader:
        if row != []:
            # delete prefix for AIS
            search_string = row[0]
            # Find the index of the first opening parenthesis
            index_of_open_parenthesis = search_string.find("(")
            search_string = search_string[index_of_open_parenthesis:]

            driver.get("https://www.webofscience.com/wos/woscc/basic-search")
            sleep(5)

            search_within = driver.find_elements(
                By.TAG_NAME, "wos-select")[2]
            search_within.click()
            sleep(0.8)
            all_options = search_within.find_elements(
                By.TAG_NAME, "div")
            for option in all_options:
                if is_title and option.text == "Title":
                    option.click()
                    is_title = False
                    break
                elif not is_title and option.text == "Abstract":
                    option.click()
                    is_title = True
                    break
            sleep(0.5)

            # apply search strings
            # search_form = driver.find_element(By.ID, "searchBoxZone")
            search_bar = driver.find_elements(By.ID, "mat-input-0")[0]
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)
            # sleep(10)

            # Read
            start_time = time.time()
            results = None
            while time.time() <= start_time + 12:
                try:
                    # result_div = driver.find_element(
                    #     By.ID, "results-sub-header")
                    results = driver.find_element(
                        By.CSS_SELECTOR, ".brand-blue")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            with open("data/search_results_wos.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((row[0], "err"))
                else:
                    # position = results.text.find("of")
                    # hits = results.text[position:].split()[1]
                    hits = results.text
                    writer.writerow((row[0], hits))

        else:
            # remove cookie banner, but only on the first visit
            driver.get("https://www.webofscience.com/wos/woscc/basic-search")
            sleep(6)

            reject_button = driver.find_element(
                By.ID, "onetrust-reject-all-handler")
            reject_button.click()
            sleep(1)

    driver.close()