import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from time import sleep

# Function to check if a WebElement is clickable


def is_element_clickable(driver, locator):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        return True
    except Exception:
        return False


# Read search strings
is_title = True
with open("data/search_strings.csv", "r+", newline="") as csvf:
    reader = csv.reader(csvf, delimiter=",")
    driver = webdriver.Firefox()
    for row in reader:
        if row != []:
            # delete prefix for ACM
            search_string = row[0]
            # Find the index of the first opening parenthesis
            index_of_open_parenthesis = search_string.find("(")
            search_string = search_string[index_of_open_parenthesis:]

            # set search parameters
            driver.get("https://dl.acm.org/search/advanced")
            sleep(2)
            search_within = driver.find_element(
                By.ID, "searchArea1")
            all_options = search_within.find_elements(By.TAG_NAME, "option")
            # Select either title or abstract to search for
            for option in all_options:
                if is_title and option.text == "Title":
                    option.click()
                    is_title = False
                    break
                elif not is_title and option.text == "Abstract":
                    option.click()
                    is_title = True
                    break
            sleep(2)

            # apply search strings

            # search_form = driver.find_element(By.ID, "searchBoxZone")
            search_bar = driver.find_elements(By.ID, "text1")[0]
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)
            # sleep(10)

            # Read
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

                    results = driver.find_element(
                        By.CSS_SELECTOR, ".hitsLength")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            with open("data/search_results_acm.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((row[0], "0"))
                else:
                    hits = results.text
                    writer.writerow((row[0], hits))
        else:
            # accept cookies
            driver.get("https://dl.acm.org/search/advanced")
            sleep(2)
            driver.find_element(
                By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll").click()
    driver.close()
