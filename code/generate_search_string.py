
# defining search string parts
trust_part = ["(Trust* OR Ethic* OR Responsible)",
              "Trustworthy", "(Trustworth* OR Responsible)"]
ai_part = ["((Artificial AND Intelligence) OR AI)",
           "((Artificial AND Intelligence) OR AI OR ML OR (Machine AND Learning))"]
platform_part = ["Platform", "Development", "Development AND Platform"]

genAI_part = [
    "", "NOT (generative OR Transformer* OR ChatGPT OR (Large AND Language AND Model))"]
property_part = ["", "characteristic*", "(trade-off* OR tradeoff*)",
                 "(trade-off* OR tradeoff* OR characteristic*)", "(trade-off* OR tradeoff*) AND characteristic*"]

combination_list = []

# logic to build search strings
for tp in trust_part:
    for ai in ai_part:
        for plat in platform_part:
            for gen in genAI_part:
                for prop in property_part:
                    # build search string for Title and Abstract directly
                    # after each other
                    search_string = "\nTITLE("
                    search_string += tp + " AND " + ai + " AND " + plat
                    if prop != "":
                        search_string += " AND " + prop
                    if gen != "":
                        search_string += " " + gen
                    search_string += ")"
                    combination_list.append(search_string)

                    search_string = "\nABSTRACT("
                    search_string += tp + " AND " + ai + " AND " + plat
                    if prop != "":
                        search_string += " AND " + prop
                    if gen != "":
                        search_string += " " + gen
                    search_string += ")"
                    combination_list.append(search_string)

with open("data/search_strings.csv", "w+") as f:
    f.writelines(combination_list)
