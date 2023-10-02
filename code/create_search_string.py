# This script creates search string and writes them into text files.

# imports
from itertools import product

# define your search string components:
# text blocks within an inner list are not combined in one string, but are used rotationally
# The blocks from the inner lists are connected with an AND in the final search string
# use empty strings to make parts optional
# "NOT"-clauses you be inserted last
# NOTE: Wildcards and logical operators need to be supported by the database engine
input_list = [
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


def create_search_string(input_list: list, fields_to_search: list, database: str):
    input_list.insert(0, fields_to_search)
    # combine the components to get all possible combinations
    combinations = list(product(*input_list))
    search_string_list = []
    if database.lower() in ["acm", "web of science", "ais", "ebscohost", "proquest"]:
        for combi in combinations:
            search_string = "\n" + combi[0] + "("
            for combi_index in range(1, len(combi)):
                if combi[combi_index] != "":
                    search_string += " AND " + combi[combi_index]

            search_string += ")"
            # replace "AND NOT" to "NOT"
            search_string = search_string.replace("AND NOT", "NOT")
            # replace "(AND" to "(" at the beginning of search string
            search_string = search_string.replace("( AND ", "(")

            search_string_list.append(search_string)

    elif database.lower() == "ieeexplore":
        pass
    else:
        print("INFO: You specified a not known database. The standard string generation method is used. The search string might not work.")
        return create_search_string(input_list, fields_to_search, "acm")

    out_file_name = "data/search_strings_" + database.lower() + ".txt"
    with open(out_file_name, "w+") as f:
        f.writelines(search_string_list)

    return


if __name__ == "__main__":
    create_search_string(input_list, fields_to_search, "proquest")
