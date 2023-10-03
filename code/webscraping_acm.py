import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep


def is_element_clickable(driver, locator, timeout=10):
    """Function to check if a WebElement is clickable
    It waits max timeout seconds until it returns that element is not clickable"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return True
    except Exception:
        return False


# Read search strings
with open("data/search_strings_acm.txt", "r+") as in_file:
    # define webdriver for browser
    driver = webdriver.Firefox()
    for line in in_file:
        line = line.strip()
        if line != "":
            # Extract search field for ACM
            # Find the index of the first opening parenthesis
            index_of_open_parenthesis = line.find("(")
            search_field = line[:index_of_open_parenthesis]
            search_string = line[index_of_open_parenthesis:]

            driver.get("https://dl.acm.org/search/advanced")
            sleep(2)
            # set search parameters: set search field
            search_within = driver.find_element(
                By.ID, "searchArea1")
            all_options = search_within.find_elements(By.TAG_NAME, "option")
            # Select the right search field to search in
            for option in all_options:
                if search_field.lower() == option.text.lower():
                    option.click()
                    break
            sleep(1)

            # apply search strings
            search_bar = driver.find_elements(By.ID, "text1")[0]
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)
            # sleep(10)

            # Read number of results
            # Try for 12 seconds until save fail
            start_time = time.time()
            results = None
            while time.time() <= start_time + 12:
                try:
                    # select only research articles as content type:
                    if is_element_clickable(driver, (By.LINK_TEXT, "Content Type")):
                        driver.find_element(
                            By.LINK_TEXT, "Content Type").click()
                        sleep(1)
                        drop_menu = driver.find_element(By.ID, "ContentType")
                        limitators = drop_menu.find_elements(
                            By.TAG_NAME, "a")
                        clicked = False
                        for limitator in limitators:
                            if "Research Article" in limitator.text:
                                limitator.click()
                                clicked = True
                                break
                        if not clicked:
                            break
                    else:
                        break
                    sleep(2)

                    # get number of results
                    results = driver.find_element(
                        By.CSS_SELECTOR, ".hitsLength")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            # write results directly together with search string into csv file
            with open("data/search_results_acm.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((line, "0"))
                else:
                    hits = results.text
                    writer.writerow((line, hits))
        else:
            # accept cookies when opening site first
            driver.get("https://dl.acm.org/search/advanced")
            sleep(2)
            driver.find_element(
                By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll").click()
    driver.close()
