import argparse
import random

import colorama
import requests
from hentai import Format, Hentai, Utils

parser = argparse.ArgumentParser(
    description="Doujins downloader from https://www.nhentai.net",
    epilog="Enjoy the program! :)",
)

parser.add_argument(
    "-r", "--random", dest="random", help="Random doujin", action="store_true"
)
parser.add_argument("-id", dest="id", type=int, help="Doujin id", action="store")
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
    "-visual", dest="visual", help="Use the 'visual' mode", action="store_true"
)


args = parser.parse_args()


def id_doujin(doujin_id):
    # Check that the doujin exists
    try:
        doujin = Hentai(doujin_id)
    except requests.exceptions.HTTPError:
        print(f"[{colorama.Fore.RED}X{colorama.Fore.WHITE}] The doujin does not exist")
        exit()

    # Doujin's title
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Title: {doujin.title(Format.Pretty)}\n"
    )

    if args.download:
        download(doujin)

    return doujin


# Display the doujin's informations
def details(doujin):
    # Display the doujin's tags
    tags = []
    try:
        for tag in doujin.tag:
            tags.append(f"{tag.name}")
    except IndexError:
        pass
    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Tag:   {tags[0]}")
    tags.pop(0)
    for tag in tags:
        print(f"           {tag}")

    # Display the Artist info
    try:
        art_info_str = str(doujin.artist[0])
    except IndexError:
        pass

    """

         The "doujin.artist" response is a type object, which I convereted
         in a string and extracted all the informations I wanted

    """

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

    if args.download:
        download(doujin)


def random_doujin():
    cringy_phrases = [
        "Look at what I found",
        "Hmmmmm",
        "Yummy ;)",
        "OMG this is fantastic!!!",
        "Ya-yamete kudasai onii-chan",
    ]
    # Get a random phrase
    phrase = random.choices(cringy_phrases)[0]

    # Get a randon ID
    rand_hnt = Utils.get_random_id()

    doujin = Hentai(rand_hnt)

    # Doujin's title
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] {phrase}:   {doujin.title(Format.Pretty)}\n"
    )
    return doujin


# View the source images
def source(doujin):
    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Source:")
    for image in doujin.image_urls:
        print(f"            {image}")
    if args.download:
        download(doujin)


# Download the doujin
def download(doujin):
    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}]")
    doujin.download(progressbar=True)


def func_query(interest, query):
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Some {query} doujins 4 u!\n"
    )
    for doujin in Utils.search_by_query(f"{interest}:{query}"):
        print(f"\ {doujin.title(Format.Pretty)}")


# Visual part
def menu():
    if args.visual:
        print(
            f"\n[{colorama.Fore.YELLOW}?{colorama.Fore.WHITE}] What do you want to do? [1-3]\n"
        )
        print("1) Search by id")
        print("2) Get a random doujin")
        print("3) Advanced query")
        print("4) Exit")
        choice = int(input("\nChoice: "))
        print("\n")
        if choice == 1:
            print("SEARCH BY ID\n")
            doujin_id = int(input("Doujin id: "))
            ask_det = input("Do you want to see the details (y/n)? ")
            if ask_det == "y":
                doujin = id_doujin(doujin_id)
                details(doujin)
            else:
                doujin = id_doujin(doujin_id)
            ask_down = input("Do you want to download the doujin (y/n)? ")
            if ask_down == "y":
                download(doujin)
                menu()
            else:
                menu()

        elif choice == 2:
            print("RANDOM DOUJIN\n")
            ask_det = input("Do you want to see the details (y/n)? ")
            if ask_det == "y":
                doujin = random_doujin()
                details(doujin)
            else:
                doujin = random_doujin()
            ask_down = input("Do you want to download the doujin (y/n)? ")
            if ask_down == "y":
                download(doujin)
                menu()
            else:
                menu()
        elif choice == 3:
            print("ADVANCED QUERY\n")
            interest = input("Write your interest (tag, character...): ")
            query = input("Query: ")
            func_query(interest, query)
            menu()

        elif choice == 4:
            print("Bye :)")
            exit()


if __name__ == "__main__":

    print("    __ _                _          ")
    print("  /\ \ \ |__   ___ _ __ | |_ _   _ ")
    print(" /  \/ / '_ \ / _ \ '_ \| __| | | |")
    print("/ /\  /| | | |  __/ | | | |_| |_| |")
    print("\_\ \/ |_| |_|\___|_| |_|\__|\__, |")
    print("                             |___/ ")

    menu()

    # CLI part
    if args.random:
        doujin = random_doujin()

        if args.details:
            details(doujin)

        elif args.download:
            download(doujin)

        elif args.source:
            source(doujin)

    elif args.id:
        doujin_id = args.id
        doujin = id_doujin(doujin_id)

        if args.details:
            details(doujin)

        elif args.source:
            source(doujin)

    elif args.query:
        if args.interest:
            interest = args.interest
            query = interest.query
            func_query(interest, query)
        else:
            print(
                f"[{colorama.Fore.RED}X{colorama.Fore.WHITE}] You must specify your area of interest (tag, character...)\n    Use the option -h for help"
            )
