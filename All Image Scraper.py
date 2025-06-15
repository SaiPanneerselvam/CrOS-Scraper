import requests
from bs4 import BeautifulSoup
import os
import time
print("Welcome to a more complicated RMA-Scraper. This tool instead scrapes all the recovery images and RMA SHIM links from chrome100.dev's website at once, and can display links quickly.")

boardnames = [
    "ambassador", "arkham", "asuka", "asurada", "atlas", "auron-paine", "auron-yuna", "banjo", "banon", "bob", "brask",
    "brya", "buddy", "buddy-cfm", "butterfly", "candy", "caroline", "cave", "celes", "chell", "cherry", "clapper",
    "constitution", "coral", "corsola", "cyan", "daisy", "daisy-skate", "daisy-spring", "dedede", "drallion", "edgar",
    "elm", "endeavour", "enguarde", "eve", "excelsior", "expresso", "falco", "falco-li", "fizz", "fizz-cfm", "gale",
    "gandof", "geralt", "glimmer", "gnawty", "grunt", "guado", "guado-cfm", "guybrush", "hana", "hatch", "heli",
    "jacuzzi", "kalista", "kalista-cfm", "kefka", "kevin", "kip", "kukui", "lars", "leon", "link", "lulu", "lumpy",
    "mccloud", "monroe", "nami", "nautilus", "ninja", "nissa", "nocturne", "nyan-big", "nyan-blaze", "nyan-kitty",
    "octopus", "orco", "panther", "parrot-ivb", "peach-pi", "peach-pit", "peppy", "puff", "pyro", "quawks", "rammus",
    "reef", "reks", "relm", "reven", "rex", "rikku", "rikku-cfm", "samus", "sand", "sarien", "scarlet", "sentry",
    "setzer", "skyrim", "snappy", "soraka", "squawks", "staryu", "stout", "strongbad", "stumpy", "sumo", "swanky",
    "terra", "tidus", "tricky", "trogdor", "ultima", "veyron-fievel", "veyron-jaq", "veyron-jerry", "veyron-mickey",
    "veyron-mighty", "veyron-minnie", "veyron-speedy", "veyron-tiger", "volteer", "whirlwind", "winky", "wizpig",
    "wolf", "x86-alex", "x86-alex-he", "x86-mario", "x86-zgb", "x86-zgb-he", "zako", "zork"
]

all_data = {}

print("Scraping and displaying all data...\n")

for board in boardnames:
    url = f"https://chrome100.dev/board/{board}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            continue
    except requests.exceptions.RequestException:
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    recovery_images_output = []
    rma_shim_output = []

    table = soup.find("table")
    if table:
        for row in table.find_all("tr"):
            chrome_version = row.get("data-chrome", "Unknown")
            download_tag = row.find("a", string="Download")
            if download_tag and download_tag.has_attr("href"):
                recovery_images_output.append({
                    "chrome_version": chrome_version,
                    "download_url": download_tag["href"]
                })

    rma_shim_header = soup.find("h2", string="RMA Shim")
    if rma_shim_header:
        rma_shim_list = rma_shim_header.find_next_sibling("ul")
        if rma_shim_list:
            for a in rma_shim_list.find_all("a"):
                if a.has_attr("href"):
                    rma_shim_output.append(a["href"])

    all_data[board] = {
        "recovery": recovery_images_output,
        "rma": rma_shim_output
    }

    print(f"Board: {board}")
    if rma_shim_output:
        print("  RMA SHIM:")
        for link in rma_shim_output:
            print(f"    {link}")

    if recovery_images_output:
        print("  RECOVERY IMAGES:")
        for entry in recovery_images_output:
            print(f"    Chrome Version: {entry['chrome_version']} | Download: {entry['download_url']}")
    if not recovery_images_output and not rma_shim_output:
        print("  No downloads found.")

    print("-" * 40)

input("Press Enter to continue...")

os.system("cls" if os.name == "nt" else "clear")

while True:
    board_input = input("Enter board name (or 'exit' to quit): ").strip().lower()
    if board_input == "exit":
        break

    version_input = input("Enter ChromeOS version (e.g. 113): ").strip()

    if board_input in all_data:
        board_data = all_data[board_input]
        recovery = board_data["recovery"]
        rma = board_data["rma"]

        found = False
        print("\nRecovery Images:")
        for entry in recovery:
            if entry["chrome_version"].startswith(version_input):
                print(f"  Chrome Version: {entry['chrome_version']} | Download: {entry['download_url']}")
                found = True

        if not found:
            print("  No recovery images found for that version.")

        print("\nRMA Shim Links:")
        if rma:
            for link in rma:
                print(f"  {link}")
        else:
            print("  No RMA shim found.")
    else:
        print("Board not found.")

    print("-" * 40)
