# CrOS-Scraper
3 Python Scripts that can be used to scrape ChromeOS images from Google and Chrome100.dev and manually get the URLs.

### How to use?
First, you must run some PIP install commands.
</br>
Run:
`pip install bs4`
and
`pip install requests` - If not already installed
</br>
This installs the libraries that this scraper uses via PyPi (Pip).

### Scripts
This tool has 3 Scripts
#### Shim and Recovery Scraper.py
This tool scrapes both the RMA Shim Mirrors and the Recovery Images, both in one file.
#### Recovery Scraper.py
This tool only scrapes the Recovery Images.
#### All Image Scraper.py
This tool, unlike others, scrapes ALL images and shims and once for EVERY board from a pregenerated list, and lets you pick the boardname (octopus, dedede, nissa) and then the ChromeOS version (browser version, like 97, 98, 114) and the script uses All of the images that were previously scraped to pick the image(s) that were asked for.

### Caveat
This tool was only built once and will not/does not get updates or new releases. This tool may become outdated if newer designs or website redesigns occur.


## Tool built by SaiPa!
