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
with open("data/search_strings.csv", "r+", newline="") as csvf:
    reader = csv.reader(csvf, delimiter=",")
    writer = csv.writer(csvf)
    driver = webdriver.Firefox()
    for row in reader:
        if row != []:
            search_string = row[0]
            # set search parameters
            driver.get("https://www.proquest.com")
            sleep(2)
            review_limit = driver.find_element(
                By.ID, "peerReviewLimit")
            if not review_limit.is_selected():
                review_limit.click()

            # apply search strings

            search_form = driver.find_element(By.ID, "searchBoxZone")
            search_bar = search_form.find_elements(By.ID, "searchTerm")[0]
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)
            # sleep(10)

            # Read
            start_time = time.time()
            results = None
            while time.time() <= start_time + 12:
                try:
                    # print("next try\n")
                    sleep(0.5)
                    results = driver.find_element(
                        By.ID, "pqResultsCount")
                    break
                except Exception as e:
                    # print(e)
                    continue
            with open("data/search_results_proquest.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((search_string, "err"))
                else:
                    hits = results.text.split()[0]
                    writer.writerow((search_string, hits))

        else:
            # remove cookie banner, but only on the first visit
            driver.get("https://www.proquest.com")
            sleep(2)

            reject_button = driver.find_element(
                By.ID, "onetrust-reject-all-handler")
            reject_button.click()
            sleep(1)

    driver.close()
