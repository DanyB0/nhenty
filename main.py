import argparse
import random

import colorama
from hentai import Format, Hentai, Utils

parser = argparse.ArgumentParser(
    description="Doujins downloader from https://www.nhentai.net",
    epilog="Enjoy the program! :)",
)

parser.add_argument(
    "-r", "--random", dest="random", help="Random doujin", action="store_true"
)
parser.add_argument(
    "-id", dest="id", type=int, help="Doujin id", action="store"
)
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

args = parser.parse_args()


def details():
    # Display the doujin's tags
    tags = []
    for tag in doujin.tag:
        tags.append(f"{tag.name}")
    print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Tag:   {tags[0]}")
    tags.pop(0)
    for tag in tags:
        print(f"           {tag}")
    print("\n|--------------------------------------------------------|\n")

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
        print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Artist: {artist[0]}")
        print(f"            {artist[1]}")
        print(f"            {artist[2]}")
        print(f"            {artist[3]}")
    except IndexError:
        pass


if args.random:
    cringy_phrases = [
        "Look at what I found",
        "Hmmmmm",
        "Yummy ;)",
        "OMG this is fantastic!!!",
        "Ya-yamete kudasai onii-chan",
    ]
    phrase = random.choices(cringy_phrases)[0]
    # Get a randon ID
    rand_hnt = Utils.get_random_id()
    doujin = Hentai(rand_hnt)
    # Doujin's title
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] {phrase}:   {doujin.title(Format.Pretty)}"
    )
    print("\n|--------------------------------------------------------|\n")
    details()


if args.id:
    doujin = Hentai(args.id)

    # Check that the doujin exists
    if not Hentai.exists(doujin.id):
        print(f"\n{colorama.Fore.RED}The doujin does not exist")

    # Doujin's title
    print(
        f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Title: {doujin.title(Format.Pretty)}"
    )

    print("\n|--------------------------------------------------------|\n")

    if args.details:
        details()

    if args.download:
        print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}]")
        doujin.download(progressbar=True)
        print("\n|--------------------------------------------------------|\n")

    if args.source:
        print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] Source:")
        for image in doujin.image_urls:
            print(f"            {image}")
        print("\n|--------------------------------------------------------|\n")
