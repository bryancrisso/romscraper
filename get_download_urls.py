from bs4 import BeautifulSoup
import requests

root_url = "https://r-roms.github.io/"

root_page = requests.get(root_url)

root_soup = BeautifulSoup(root_page.content, "html.parser")

root_hrefs = root_soup.find_all("a", href=True)

chosen_categories = []
chosen_systems = []

with open("categories.txt", "r") as f:
    chosen_categories = f.read().splitlines()

with open("systems.txt", "r") as f:
    chosen_systems = f.read().splitlines()

category_urls_unfiltered = [(link["href"], category) for link in root_hrefs for category in chosen_categories if category in link["href"]]
category_urls = set([(url.strip("/"), category) for url,category in category_urls_unfiltered])

system_urls = []
download_urls = []

for rom_url, category in category_urls:
    category_page = requests.get(root_url + rom_url)
    category_soup = BeautifulSoup(category_page.content, "html.parser")
    category_hrefs = category_soup.find_all("a", href=True)
    rom_urls = set([(link["href"], category, system) for link in category_hrefs for system in chosen_systems if ("/"+system.replace(" ", "%20")+"/") in link["href"] and "myrient" in link["href"]])
    print("\n link: ", rom_url)
    for rom_url in rom_urls:
        system_urls.append(rom_url)

for url, cat, sys in system_urls:
    system_page = requests.get(url)
    system_soup = BeautifulSoup(system_page.content, "html.parser")
    system_hrefs = system_soup.find_all("a", href=True)
    download_urls += list(set([(url, link["href"], cat, sys) for link in system_hrefs if link["href"].endswith(".zip")]))

with open("download_urls.txt", "w") as f:
    for url, file, category, sys in download_urls:
        f.write(category + "," + sys + "," +file +","+ url + file + "\n")
