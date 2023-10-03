# Literature Search String Generator and Assessment

This repo contains code to generate and assess search strings for the literature review of my master thesis. As I found it hard to come up with a meaningful and good search string, I took a systematic way:

1. There is one script constructing search strings by combining predefined text blocks
2. For each database, I want to search through, I wrote a script that uses web scraping methods to automatically use databases' web searches to obtain the number of results to assess the search string quantitative.

## Technologies and Requirements

I used mainly selenium and a pre-installed Mozilla Firefox browser (see also conda [environment-file](environment.yml)). Searched databases are: ACM Library, AIS Library, IEEE Xplore, Ebscohost, Proquest and Web of Science (WOS). The scripts assume that you have access (e.g. by VPN) to these databases. The code is tested on WSL2 on Windows 11. The search strings and the results are stored in different text and CSV files [here](/data/).

## Customization

As you can see in the [create_search_string.py](code/create_search_string.py) some of the databases expect abbreviated keywords for the search fields, some not, and some use other words than standards. Please make sure you generate the search strings with the right corresponding search fields.
