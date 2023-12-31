import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
from time import sleep


# Read search strings
with open("data/search_strings_wos.txt", "r+") as in_file:
    lines = in_file.readlines()
    # define webdriver for browser
    driver = webdriver.Firefox()
    # remove cookie banner, but only on the first visit
    driver.get("https://www.webofscience.com/wos/woscc/basic-search")
    sleep(6)

    reject_button = driver.find_element(
        By.ID, "onetrust-reject-all-handler")
    reject_button.click()
    sleep(1)
    for l_number, line in enumerate(lines):
        line = line.strip()
        if line != "":
            # Extract search field for Web of Science
            # Find the index of the first opening parenthesis
            index_of_open_parenthesis = line.find("(")
            search_field = line[:index_of_open_parenthesis]
            search_string = line[index_of_open_parenthesis:]

            driver.get("https://www.webofscience.com/wos/woscc/basic-search")
            sleep(3)

            # Select the right search field to search in
            search_within = driver.find_elements(
                By.TAG_NAME, "wos-select")[2]
            search_within.click()
            sleep(0.8)
            all_options = search_within.find_elements(
                By.TAG_NAME, "div")
            for option in all_options:
                if search_field.lower() == option.text.lower():
                    option.click()
                    break
            sleep(0.5)

            # apply search strings
            search_bar = driver.find_elements(By.ID, "mat-input-0")[0]
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
                        By.CSS_SELECTOR, ".brand-blue")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            # write results directly together with search string into csv file
            with open("data/search_results_wos.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((line, "0"))
                else:
                    hits = results.text
                    writer.writerow((line, hits))
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
