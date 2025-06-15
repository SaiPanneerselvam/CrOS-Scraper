import requests
from bs4 import BeautifulSoup
print("Welcome to RMA-Scraper. This tool scrapes recovery images and RMA SHIM links from chrome100.dev's website.")
print("Starting the scraper...")
real = input("Please enter the boardname (octopus, dedede, nissa): ").strip().lower()

url = "https://chrome100.dev/board/" + real

try:
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print(f"Error: Boardname '{real}' does not exist or page not found (HTTP Status: {response.status_code}).")
        exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: Unable to connect to the server or WiFi issue: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

recovery_images_output = []
rma_shim_output = []

table = soup.find("table")
if table:
    rows = table.find_all("tr")
    for row in rows:
        chrome_version = row.get("data-chrome", "Unknown Chrome Version")
        download_tag = row.find("a", string="Download")
        download_url = "N/A"
        if download_tag and download_tag.has_attr("href"):
            download_url = download_tag["href"]
        if download_url != "N/A":
            recovery_images_output.append({
                "chrome_version": chrome_version,
                "download_url": download_url,
            })

rma_shim_header = soup.find("h2", string="RMA Shim")
if rma_shim_header:
    rma_shim_list = rma_shim_header.find_next_sibling("ul")
    if rma_shim_list:
        rma_shim_links = rma_shim_list.find_all("a")
        for link_tag in rma_shim_links:
            if link_tag.has_attr("href"):
                rma_shim_output.append(link_tag["href"])

if rma_shim_output:
    print("RMA SHIM ------")
    for link in rma_shim_output:
        print(link)
    print()

if recovery_images_output:
    print("RECOVERY IMAGES ----")
    for entry in recovery_images_output:
        print(f"Chrome Version: {entry['chrome_version']} | Download: {entry['download_url']}")
    print()

if not recovery_images_output and not rma_shim_output:
    print("No download links (recovery or RMA SHIM) found for the specified boardname.")

print("Scraping finished.")
