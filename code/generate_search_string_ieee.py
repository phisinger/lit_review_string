# defining search string parts
# As IEEE expects the search field (Title or Abstract) always directly
# before the search term, XY is a placeholder which later replaced.
trust_part = ["(XYTrust* OR XYEthic* OR XYResponsib*)",
              "XYTrustworthy", "(XYTrustworth* OR XYResponsib*)"]
ai_part = ["((XYArtificial AND XYIntelligence) OR XYAI)",
           "((XYArtificial AND XYIntelligence) OR XYAI OR XYML OR (XYMachine AND XYLearning))"]
platform_part = ["XYPlatform", "XYDevelopment", "XYDevelopment AND XYPlatform"]
location_part = ["Document Title", "Abstract"]

genAI_part = [
    "", "NOT (XYgenerative OR XYTransformer* OR XYChatGPT OR (XYLarge AND XYLanguage AND XYModel))"]
property_part = ["", "XYcharacteristic*", "(XYtrade-off* OR XYtradeoff*)",
                 "(XYtrade-off* OR XYtradeoff* OR XYcharacteristic*)", "(XYtrade-off* OR XYtradeoff*) AND XYcharacteristic*"]

combination_list = []

# logic to build search strings
for tp in trust_part:
    for ai in ai_part:
        for plat in platform_part:
            for gen in genAI_part:
                for prop in property_part:
                    for location in location_part:
                        search_string = "\n" + tp + " AND " + ai + " AND " + plat
                        if prop != "":
                            search_string += " AND " + prop
                        if gen != "":
                            search_string += " " + gen
                        print("before replacement: ", search_string)
                        # define placeholder replacement and replace
                        new_string = "\"" + location + "\":"
                        search_string = search_string.replace("XY", new_string)
                        print("after replacement: ", search_string)

                        combination_list.append(search_string)

    # print(search_string)

# write all search string to csv file
with open("data/search_strings_ieee.txt", "w+",) as f:
    f.writelines(combination_list)
