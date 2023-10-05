import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep


def is_error_message(driver, timeout=10):
    """Function to check if a WebElement is on the page
    It waits max timeout seconds until it returns that element is not on the page"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.ID, "ctl00_ctl00_MainContentArea_MainContentArea_smartTextRanWarning"))
        )
        # If the element is found, return True
        return True
    except Exception:
        return False


# Read search strings
with open("data/search_strings_ebscohost.txt", "r+") as in_file:
    lines = in_file.readlines()
    # define webdriver for browser
    driver = webdriver.Firefox()
    for l_number, line in enumerate(lines):
        line = line.strip()
        if line != "":
            # Navigate to the real search
            driver.get("https://search.ebscohost.com")
            driver.find_element(By.LINK_TEXT, "EBSCOhost Web").click()
            sleep(2)
            driver.find_element(
                By.ID, "ctl00_ctl00_MainContentArea_MainContentArea_Eplabel1").click()
            driver.find_element(
                By.ID, "ctl00_ctl00_MainContentArea_MainContentArea_continue1").click()
            sleep(2)

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
            search_bar.send_keys(line)
            search_bar.send_keys(Keys.RETURN)

            # Read number of results
            # Try for 12 seconds until save fail
            start_time = time.time()
            results = None
            while time.time() <= start_time + 12:
                try:
                    # Catch ebsohost error warning
                    if is_error_message(driver):
                        break
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
                    writer.writerow((line, "0"))
                else:
                    writer.writerow((line, results.text.split()[-1]))
        # After the search result is successfully written,
        # the search string is deleted from the search_string file.
        # move file pointer to the beginning of a file
        in_file.seek(0)
        # truncate the file
        in_file.truncate()
        try:
            in_file.writelines(lines[l_number+1:])
        except:
            pass
    driver.close()
