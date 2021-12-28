#!/usr/bin/env python

import argparse
import os
import random
import webbrowser
import tqdm

import bs4
import colorama
import requests
from hentai import Format, Hentai, Utils

parser = argparse.ArgumentParser(
    description="Doujins downloader from https://nhentai.net",
    epilog="Enjoy the program! :)",
)

parser.add_argument(
    "-r", "--random", dest="random", help="Random doujin", action="store_true"
)

parser.add_argument("-id", dest="id", type=str, help="Doujin id", action="store")

parser.add_argument(
    "-dtls",
    "--details",
    dest="details",
    help="Display the doujin's details",
    action="store_true",
)
parser.add_argument(
    "-d", "--download", dest="download", help="Download the doujin", action="store_true"
)

parser.add_argument(
    "-src",
    "--source",
    dest="source",
    help="View the link to the images",
    action="store_true",
)

parser.add_argument(
    "-i",
    "--interest",
    dest="interest",
    help="Area of interest (ex.character, tag...)",
    action="store",
)

parser.add_argument("-q", "--query", dest="query", help="Query", action="store")

parser.add_argument(
    "-w", "--web", dest="web", help="Open doujin in browser", action="store_true"
)

parser.add_argument(
    "--visual", dest="visual", help="Use the 'visual' mode", action="store_true"
)


args = parser.parse_args()


def id_doujin(doujin_id):
    # Check that the doujin exists
    try:
        doujin = Hentai(doujin_id)
    except requests.exceptions.HTTPError:
        print(
            f"\n[{colorama.Fore.RED}X{colorama.Fore.WHITE}] The doujin does not exist"
        )
        menu(BASE_URL)

    # Doujin's title
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Title: {doujin.title(Format.Pretty)}"
    )

    if args.download:
        download(doujin, BASE_URL, BASE_DIR)

    return doujin


# Display the doujin's informations
def details(doujin, BASE_URL):
    # Display the doujin's tags
    tags = []
    try:
        for tag in doujin.tag:
            tags.append(f"{tag.name}")
    except IndexError:
        pass
    try:
        print(f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Tag:   {tags[0]}")
    except IndexError:
        pass
    tags.pop(0)
    for tag in tags:
        print(f"           {tag}")

    # Display the Artist info
    try:
        art_info_str = str(doujin.artist[0])
    except IndexError:
        pass

    # The "doujin.artist" response is a type object, which I convereted
    # in a string and extracted all the informations I wanted
    try:
        art_info_str = art_info_str[4:-1].replace(" ", "")
    except UnboundLocalError:
        exit()
    art_info = []
    for i in range(len(art_info_str)):
        try:
            if art_info_str[i] == ",":
                info = art_info_str[:i]
                art_info.append(info)
                art_info_str = art_info_str.replace(f"{info},", "")
        except IndexError:
            pass

    artist = []
    for info in art_info:
        info = info.replace("=", " = ")
        artist.append(info)
    try:
        print(f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Other: {artist[0]}")
        print(f"           {artist[1]}")
        print(f"           {artist[2]}")
        print(f"           {artist[3]}")
    except IndexError:
        pass

    if args.web:
        open_web(doujin, BASE_URL)

    if args.download:
        download(doujin, BASE_URL, BASE_DIR)


def random_doujin():
    # Get a randon ID
    rand_hnt = Utils.get_random_id()

    doujin = Hentai(rand_hnt)

    # Doujin's title
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Title: {doujin.title(Format.Pretty)}\n"
    )
    return doujin


# View the source images
def source(doujin, BASE_URL):
    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Source:")
    for image in doujin.image_urls:
        print(f"            {image}")

    if args.web:
        open_web(doujin, BASE_URL)

    if args.download:
        download(doujin, BASE_URL, BASE_DIR)


# Download the doujin
def download(doujin, BASE_URL, BASE_DIR):
    if not os.path.exists(str(doujin.id)):
        os.mkdir(str(doujin.id))
        os.chdir(str(doujin.id))
    else:
        print(f"[{colorama.Fore.RED}X{colorama.Fore.WHITE}] The folder already exists")
        exit()
    print(f"\n[{colorama.Fore.YELLOW}...{colorama.Fore.WHITE}] Downloading...")
    url = BASE_URL + str(doujin.id)
    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    image = soup.findAll("img")

    for i in range(len(image)):
        image_url = image[i]["src"]
        if not image_url.startswith("data"):
            r = requests.get(image_url).content
            with open(f"{i//2}.png", "wb+") as f:
                f.write(r)
        pass
    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Download complete")
    os.chdir(BASE_DIR)


# Advanced search
def func_query(interest, query):
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Some {query} doujins 4 u!\n"
    )
    for doujin in Utils.search_by_query(f"{interest}:{query}"):
        print(f"\ {doujin.title(Format.Pretty)}")


# open link in browser
def open_web(doujin, BASE_URL):
    print(f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Opening browser...")
    webbrowser.open(BASE_URL + str(doujin.id))


# Visual part
def menu(BASE_URL):
    if args.visual:
        print(
            f"\n[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] What do you want to do? [1-4]\n"
        )
        print("1) Search by id")
        print("2) Get a random doujin")
        print("3) Advanced query")
        print("4) Exit")
        choice = input("\nChoice: ")
        try:
            choice = int(choice)
        except ValueError:
            print(
                f"\n[{colorama.Fore.RED}X{colorama.Fore.WHITE}] You must select a number"
            )
            menu(BASE_URL)
        print("\n")
        if choice == 1:
            print("SEARCH BY ID\n")
            # Check that the id is a number
            try:
                doujin_id = int(input("Doujin id: "))
            except ValueError:
                print(
                    f"\n[{colorama.Fore.RED}X{colorama.Fore.WHITE}] The id must be a number"
                )
                menu()
            ask_det = input(
                f"[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] Do you want to see the details (y/N)? "
            )
            if ask_det == "y":
                doujin = id_doujin(doujin_id)
                details(doujin, BASE_URL)
            else:
                doujin = id_doujin(doujin_id)
            ask_down = input(
                f"\n[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] Do you want to download the doujin (y/N)? "
            )
            ask_web = input(
                f"\n[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] Do you want to open the doujin in the browser (y/N)? "
            )
            if ask_web == "y":
                if ask_down == "y":
                    download(doujin, BASE_URL, BASE_DIR)
                    open_web(doujin, BASE_URL)
                    menu(BASE_URL)
                else:
                    open_web(doujin, BASE_URL)
                    menu(BASE_URL)
            else:
                if ask_down == "y":
                    download(doujin, BASE_URL, BASE_DIR)
                    # open_web(doujin, BASE_URL)
                    menu(BASE_URL)
                else:
                    menu(BASE_URL)

        elif choice == 2:
            print("RANDOM DOUJIN\n")
            ask_det = input(
                f"[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] Do you want to see the details (y/N)? "
            )
            if ask_det == "y":
                doujin = random_doujin()
                details(doujin, BASE_URL)
            else:
                doujin = random_doujin()
            ask_down = input(
                f"\n[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] Do you want to download the doujin (y/N)? "
            )
            ask_web = input(
                f"\n[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] Do you want to open the doujin in the browser (y/N)? "
            )
            if ask_web == "y":
                if ask_down == "y":
                    download(doujin, BASE_URL, BASE_DIR)
                    open_web(doujin, BASE_URL)
                    menu(BASE_URL)
                else:
                    open_web(doujin, BASE_URL)
                    menu(BASE_URL)
            else:
                if ask_down == "y":
                    download(doujin, BASE_URL, BASE_DIR)
                    open_web(doujin, BASE_URL)
                    menu(BASE_URL)
                else:
                    menu(BASE_URL)

        elif choice == 3:
            print("ADVANCED QUERY\n")
            interest = input("Write your interest (tag, character...): ")
            query = input("Query: ")
            func_query(interest, query)
            menu(BASE_URL)

        elif choice == 4:
            print("Bye :)")
            exit()


if __name__ == "__main__":

    BASE_URL = "https://nhentai.net/g/"
    BASE_DIR = os.getcwd()

    print("     __ _                _          ")
    print("  /\ \ \ |__   ___ _ __ | |_ _   _ ")
    print(" /  \/ / '_ \ / _ \ '_ \| __| | | |")
    print("/ /\  /| | | |  __/ | | | |_| |_| |")
    print("\_\ \/ |_| |_|\___|_| |_|\__|\__, |")
    print("                             |___/ ")

    menu(BASE_URL)

    # CLI part
    if args.random:
        doujin = random_doujin()

        if args.details:
            details(doujin, BASE_URL)

        elif args.download:
            download(doujin, BASE_URL, BASE_DIR)

        elif args.source:
            source(doujin, BASE_URL)

        elif args.web:
            open_web(doujin, BASE_URL)

    elif args.id:
        doujin_id = args.id
        # Check that the id is a number
        try:
            doujin_id = int(doujin_id)
        except ValueError:
            print(
                f"\n[{colorama.Fore.RED}X{colorama.Fore.WHITE}] The id must be a number"
            )
            exit()

        doujin = id_doujin(doujin_id)

        if args.details:
            details(doujin, BASE_URL)

        elif args.source:
            source(doujin, BASE_URL)

        elif args.web:
            open_web(doujin, BASE_URL)

    elif args.query:
        if args.interest:
            interest = args.interest
            query = interest.query
            func_query(interest, query)
        else:
            print(
                f"[{colorama.Fore.RED}X{colorama.Fore.WHITE}] You must specify your area of interest (tag, character...)\n    Use the option -h for help"
            )
