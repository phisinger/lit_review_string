import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

from time import sleep

is_title = True
# Read search strings
with open("data/search_strings_ais.txt", "r+") as in_file:
    lines = in_file.readlines()
    # define webdriver for browser
    driver = webdriver.Firefox()
    for l_number, line in enumerate(lines):
        line = line.strip()
        if line != "":
            # Extract search field for AIS
            # Find the index of the first opening parenthesis
            index_of_open_parenthesis = line.find("(")
            search_field = line[:index_of_open_parenthesis]
            search_string = line[index_of_open_parenthesis:]

            driver.get("https://aisel.aisnet.org/do/search/advanced")
            sleep(2)
            # set search parameters
            # set peer reviewed
            review_limit = driver.find_element(
                By.ID, "peer-reviewed")
            if not review_limit.is_selected():
                review_limit.click()
            # Select the right search field to search in
            search_within = driver.find_element(
                By.ID, "field_1")
            all_options = search_within.find_elements(By.TAG_NAME, "option")
            for option in all_options:
                if search_field.lower() == option.text.lower():
                    option.click()
                    break
            # select database
            search_database = driver.find_element(
                By.ID, "advanced-context")
            db_all_options = search_database.find_elements(
                By.TAG_NAME, "option")
            for option in db_all_options:
                if option.text == "All Repositories":
                    option.click()
                    break
            sleep(0.5)

            # apply search strings
            search_bar = driver.find_elements(By.ID, "value_1")[0]
            search_bar.clear()
            search_bar.send_keys(search_string)
            search_bar.send_keys(Keys.RETURN)

            # Read number of results
            # Try for 12 seconds until save fail
            start_time = time.time()
            results = None
            while time.time() <= start_time + 12:
                try:
                    result_div = driver.find_element(
                        By.ID, "results-sub-header")
                    results = result_div.find_element(
                        By.CSS_SELECTOR, ".grid_6")
                    sleep(0.5)
                    break
                except Exception as e:
                    # print(e)
                    continue
            # write results directly together with search string into csv file
            with open("data/search_results_ais.csv", "a+", newline="") as csvw:
                writer = csv.writer(csvw, delimiter=";")
                if results == None:
                    writer.writerow((line, "0"))
                else:
                    position = results.text.find("of")
                    hits = results.text[position:].split()[1]
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
