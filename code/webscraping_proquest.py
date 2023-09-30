import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep

# Read search strings
with open("data/search_strings.csv", "r+", newline="") as csvf:
    reader = csv.reader(csvf, delimiter=",")
    # define webdriver for browser
    driver = webdriver.Firefox()
    for row in reader:
        if row != []:
            search_string = row[0]
            # set search parameters
            # set peer-reviewed
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

            # Read number of results
            # Try for 12 seconds until save fail
            start_time = time.time()
            results = None
            while time.time() <= start_time + 12:
                try:
                    results = driver.find_element(
                        By.ID, "pqResultsCount")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            # write results directly together with search string into csv file
            with open("data/search_results_proquest.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((search_string, "0"))
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
