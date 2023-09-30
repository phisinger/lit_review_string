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
            # prepare search string
            search_string = row[0]
            # Find the index of the first opening parenthesis
            index_of_open_parenthesis = search_string.find("(")
            # attach abbreviated search field
            search_string = search_string[:2] + \
                search_string[index_of_open_parenthesis:]

            # Navigate to the real search
            driver.get("https://search.ebscohost.com")
            driver.find_element(By.LINK_TEXT, "EBSCOhost Web").click()
            sleep(2)
            driver.find_element(
                By.ID, "ctl00_ctl00_MainContentArea_MainContentArea_Eplabel1").click()
            driver.find_element(
                By.ID, "ctl00_ctl00_MainContentArea_MainContentArea_continue1").click()
            sleep(4)

            # set search settings
            # unselect search expansion
            equivivalent_subjects = driver.find_element(
                By.ID, "expand_enhancedsubjectprecision")
            if equivivalent_subjects.is_selected():
                equivivalent_subjects.click()
            # select peer reviewed
            peer_reviewed = driver.find_element(
                By.ID, "common_RV")
            if not peer_reviewed.is_selected():
                peer_reviewed.click()

            # apply search strings
            search_bar = driver.find_element(By.ID, "Searchbox1")
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
                        By.CSS_SELECTOR, ".page-title")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            # write results directly together with search string into csv file
            with open("data/search_results_ebscohost.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((search_string, "0"))
                else:
                    writer.writerow((search_string, results.text.split()[-1]))
    driver.close()
