import requests
from bs4 import BeautifulSoup
import re


def build_ao3_search_url(query="", title="", creators="", revised_at="", complete="", crossover="", single_chapter="0",
                         word_count="", language_id="en", fandom_names="", rating_ids="10", character_names="",
                         relationship_names="", freeform_names="Batman+-+All+Media+Types", hits="", kudos_count="",
                         comments_count="",
                         bookmarks_count="", sort_column="_score", sort_direction="desc", page="1"):
    a = "=&work_search%5Bword_count%5D="
    base_url = "https://archiveofourown.org/works/search?commit=Search"
    params = {
        "work_search%5Bquery%5D": query,
        "work_search%5Bbookmarks_count%5D": bookmarks_count,
        "work_search%5Bcharacter_names%5D": character_names,
        "work_search%5Bcomments_count%5D": comments_count,
        "work_search%5Btitle%5D": title,
        "work_search%5Bcreators%5D": creators,
        "work_search%5Brevised_at%5D": revised_at,
        "work_search%5Bcomplete%5D": complete,
        "work_search%5Bcrossover%5D": crossover,
        "work_search%5Bsingle_chapter%5D": single_chapter,
        "work_search%5Bword_count%5D": word_count,
        "work_search%5Blanguage_id%5D": language_id,
        "work_search%5Bfandom_names%5D": fandom_names,
        "work_search%5Brating_ids%5D": rating_ids,
        "work_search%5Brelationship_names%5D": relationship_names,
        "work_search%5Bfreeform_names%5D": freeform_names,
        "work_search%5Bhits%5D": hits,
        "work_search%5Bkudos_count%5D": kudos_count,
        "work_search%5Bsort_column%5D": sort_column,
        "work_search%5Bsort_direction%5D": sort_direction,
        "page": page
    }
    # print(params)
    return base_url + "&" + "&".join(f"{key}={value}" for key, value in params.items() if value)


def getLinksFromPage(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    h4_tags = soup.find_all("h4")
    works_links = [
        link
        for h4 in h4_tags
        for link in h4.find_all("a", href=lambda href: re.match(r"/works/\d", href))
    ]
    full_links = ["https://archiveofourown.org" + link.get("href") for link in works_links]
    return full_links


def writeArrayToFile(arr, name="listofURLS"):
    with open(str(name) + ".txt", "w") as file:
        for element in arr:
            file.write(str(element) + "\n")


# Example usage
if __name__ == "__main__":
    big_list = []
    for i in range(1, 10):
        url = build_ao3_search_url(page=str(i))
        big_list.extend(getLinksFromPage(url))
    writeArrayToFile(big_list)
