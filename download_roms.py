import requests
import os
from urllib.parse import unquote
from tqdm import tqdm

rom_data = {}
root_download_path = "/run/media/bryanak/BIGBOI/bryan/roms/scraper_downloads/"

total = 0

def download_file(url, filename):
    # Send a GET request
    response = requests.get(url, stream=True)
    
    # Get the total file size
    total_size = int(response.headers.get('content-length', 0))
    
    # Open the output file and make sure we write in binary mode
    with open(filename, 'wb') as f, tqdm(
        desc=os.path.split(filename)[1],
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            progress_bar.update(size)

with open("keywords.txt", "r") as f:
    keywords = f.read().splitlines()

with open("download_urls.txt", "r") as f:
    download_urls = f.read().splitlines()
    download_urls = list(filter(lambda x: any(keyword in x for keyword in keywords), download_urls))
    total = len(download_urls)
    for url in download_urls:
        cat, sys, file, download_url = url.split(",")
        if cat not in rom_data:
            rom_data[cat] = {}
        if sys not in rom_data[cat]:
            rom_data[cat][sys] = []

        rom_data.get(cat, {}).get(sys, []).append((unquote(file), download_url))

count = 1
for cat in rom_data:
    os.makedirs(root_download_path + cat, exist_ok=True)
    for sys in rom_data[cat]:
        os.makedirs(root_download_path + cat + "/" + sys, exist_ok=True)
        print("\nDownloading for system: ", cat + "->" + sys)
        for rom,url in rom_data[cat][sys]:
            if not os.path.exists(root_download_path + cat + "/" + sys + "/" + rom):
                r = requests.get(url, allow_redirects=True)
                print(f"\nDownloading ({str(count)}/{str(total)}): {root_download_path}{cat}/{sys}/{rom}")
                # print("From: ", url)
                download_file(url, root_download_path + cat + "/" + sys + "/" + rom)
            count += 1

# r = requests.get(url, allow_redirects=True)
#
# open("rom.zip", "wb").write(r.content)
