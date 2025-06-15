import requests
from bs4 import BeautifulSoup


print("Welcome to the ChromeOS Recovery Image Scraper. This tool scrapes recovery images from chrome100.dev's website.")
print("Starting the scraper...")
real = input("Please enter the boardname (octopus, dedede, nissa): ").strip().lower()


url = "https://chrome100.dev/board/"+real
# Check if valid name/url/wifi is available
try:
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("Error: Boardname does not exist or page not found.")
        exit(1)
except requests.exceptions.RequestException:
    print("Error: WiFi error or unable to connect to the server.")
    exit(1)
soup = BeautifulSoup(response.text, "html.parser")

output = []

# get table with download links
table = soup.find("table")
if table:
    rows = table.find_all("tr")
    for row in rows:
        # get version from tr tag
        chrome_version = row.get("data-chrome", "Unknown Version")

        # get download link from a tag
        download_tag = row.find("a", string="Download")
        
        download_url = "N/A"
        if download_tag and download_tag.has_attr("href"):
            download_url = download_tag["href"]

        # add only if download exists
        if download_url != "N/A":
            output.append((chrome_version, download_url))

# write the results
for version, link in output:
    print(f"Chrome Version: {version} | Download: {link}")