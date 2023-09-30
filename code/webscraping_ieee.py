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
    # define webdriver for browser
    driver = webdriver.Firefox()
    for row in reader:
        if row != []:
            search_string = row[0]

            driver.get("https://ieeexplore.ieee.org")
            sleep(2)
            # set search parameters
            # select Journals and Magazins aka peer-review
            select_ele = driver.find_element(
                By.XPATH, "/html/body/div[5]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[1]/label/select")
            all_options = select_ele.find_elements(By.TAG_NAME, "option")
            for option in all_options:
                if option.text == "Journals & Magazines":
                    option.click()
                    break
            sleep(1)

            # apply search strings
            search_form = driver.find_element(
                By.TAG_NAME, "form")
            search_bar = search_form.find_elements(By.TAG_NAME, "input")[0]
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)

            # Read number of results
            # Try for 6 seconds until save fail
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
            # write results directly together with search string into csv file
            with open("data/search_results_ieee.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((search_string, "0"))
                else:
                    # Identify if result page contains results or not
                    position = results.text.find("of")
                    if position == -1:
                        hits = 0
                    else:
                        hits = results.text[position:].split()[1]
                    writer.writerow((search_string, hits))

    driver.close()
