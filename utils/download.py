import os
import urllib.request

import bs4
import colorama
import requests


# Download the doujin
def download_doujin(doujin_local, BASE_DIR_local, BASE_URL_local):
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
    os.chdir("downloads")
    if not os.path.exists(str(doujin_local.id)):
        os.mkdir(str(doujin_local.id))
        os.chdir(str(doujin_local.id))
    else:
        print(f"[{colorama.Fore.RED}X{colorama.Fore.WHITE}] The folder already exists")
        exit()
    print(f"\n[{colorama.Fore.YELLOW}...{colorama.Fore.WHITE}] Downloading...")
    url = BASE_URL_local + str(doujin_local.id)

    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    image = soup.findAll("img")

    for i, elem in enumerate(image):
        try:
            url_2 = f"https://nhentai.net/g/{doujin_local.id}/{i+1}"
            response = requests.get(url_2)

            soup = bs4.BeautifulSoup(response.text, "html.parser")
            image = soup.findAll("img")
            print(
                f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Image {i+1} ({url_2})"
            ) if not len(image) == 0 else None

            # download the images
            urllib.request.urlretrieve(image[1]["src"], f"{i+1}.jpg")
        except IndexError:
            pass

    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Download complete")
    os.chdir(BASE_DIR_local)
