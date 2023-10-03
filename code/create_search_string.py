# This script creates search string and writes them into text files.

# imports
from itertools import product
import re

# define your search string components:
# text blocks within an inner list are not combined in one string, but are used rotationally
# The blocks from the inner lists are connected with an AND in the final search string
# use empty strings to make parts optional
# "NOT"-clauses you be inserted last
# NOTE: Wildcards and logical operators need to be supported by the database engine
search_terms = [
    ["(Trust* OR Ethic* OR Responsible)",
     "Trustworthy", "(Trustworth* OR Responsible)"],
    ["((Artificial AND Intelligence) OR AI)",
     "((Artificial AND Intelligence) OR AI OR ML OR (Machine AND Learning))"],
    ["Platform", "Development", "Development AND Platform"],
    ["", "characteristic*", "(trade-off* OR tradeoff*)",
     "(trade-off* OR tradeoff* OR characteristic*)", "(trade-off* OR tradeoff*) AND characteristic*"],
    ["", "NOT (generative OR Transformer* OR ChatGPT OR (Large AND Language AND Model))"],
]
# Specify the Name of the fields you want to search in
# Please make sure that the names are correct for the database you want to search in
fields_to_search = ["TITLE", "ABSTRACT"]
fields_to_search_abb = ["TI", "AB"]
fields_to_search_ieee = ["Document Title", "Abstract"]


def construct_string_standard(combinations):
    search_string_list = []
    for combi in combinations:
        search_string = "\n" + combi[0] + "("
        for combi_index in range(1, len(combi)):
            if combi[combi_index] != "":
                search_string += " AND " + combi[combi_index]

        search_string += ")"

        # replace "(AND" to "(" at the beginning of search string
        search_string = search_string.replace("( AND ", "(")
        # replace "AND NOT" to "NOT"
        search_string = search_string.replace(
            "AND NOT", "NOT")
        search_string_list.append(search_string)

    return search_string_list


def construct_string_ieeexplore(combinations):
    search_string_list = []
    for combi in combinations:
        search_string = ""
        for combi_index in range(1, len(combi)):
            if combi[combi_index] != "":
                search_string += " AND " + combi[combi_index]

        # Insert line break and remove the first " AND "
        search_string = "\n" + search_string[5:]
        # Ingest the field name before every search term as ieee requires it.
        repl_string = "\"" + combi[0] + "\": \\1"
        # print(search_string)
        search_string = re.sub(
            r"(\b(?!AND\b|OR\b|NOT\b)\w)", repl_string, search_string)
        # replace "AND NOT" to "NOT"
        search_string = search_string.replace(
            "AND NOT", "NOT")
        search_string_list.append(search_string)

    return search_string_list


def create_search_string(search_terms: list, fields_to_search: list, database: str):
    # combine the components to get all possible combinations
    input_list = search_terms.copy()
    input_list.insert(0, fields_to_search)
    combinations = list(product(*input_list))

    if database.lower() == "web of science":
        database = "wos"

    if database.lower() in ["acm", "wos", "ais", "ebscohost", "proquest"]:
        search_string_list = construct_string_standard(combinations)
    elif database.lower() == "ieeexplore":
        search_string_list = construct_string_ieeexplore(combinations)
    else:
        print("INFO: You specified a not known database. The standard string generation method is used. The generated search string might not work.")
        search_string_list = construct_string_standard(combinations)

    out_file_name = "data/search_strings_" + database.lower() + ".txt"
    with open(out_file_name, "w") as f:
        f.writelines(search_string_list)

    return


if __name__ == "__main__":
    # by default strings for all databases are generated
    create_search_string(search_terms, fields_to_search_ieee, "ieeexplore")
    create_search_string(search_terms, fields_to_search, "acm")
    create_search_string(search_terms, fields_to_search, "ais")
    create_search_string(search_terms, fields_to_search_abb, "ebscohost")
    create_search_string(search_terms, fields_to_search, "proquest")
    create_search_string(search_terms, fields_to_search, "web of science")
