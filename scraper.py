# Scrapes listings from Onward State and stores new ones in "listings.txt"
# James Taddei
# 2024-10-01

import requests
from bs4 import BeautifulSoup
import re
from errors import ScrapingError

def _decode_email(code):
    """
    Takes an email that has been encoded by Cloudflare and returns the decoded email as a string.
    """
    r = int(code[:2], 16)
    email = "".join([chr(int(code[i : i + 2], 16) ^ r) for i in range(2, len(code), 2)])
    return email

def scrape_listings():
    """
    Scrapes all listings from Onward State and returns them as a list of dictionaries (listings).
    """
    # Gets the updated webpage from Onward State and checks that the request was successful
    res = requests.get("https://onwardstate.com/penn-state-football-student-ticket-exchange/")
    if (res.status_code != 200): # non-200 status code indicates an error
        raise ScrapingError
    
    # Prepares the data to be parsed
    soup = BeautifulSoup(res.content, "html.parser")
    listings = []

    # Loops through each section of the webpage inside a paragraph tag. Finds all of the ones with an email and stores
    # the relevant data as a dictionary in listings.
    for l in soup.find_all("p"):
        # Converts the line into a searchable string then looks for an email
        l = str(l)
        m = re.search('data-cfemail="(.*)"', l)
        if (m is None): # this indicates that the line is not a listing as it has no email
            continue
        email = _decode_email(m.group(1)) # decrpyts the Cloudflare encoding

        # Finds the price and game (opponent)
        m = re.search(r"wants (.*) for a (.*) \(.*\) ticket.", l)
        assert m is not None # lines with valid emails should include a price and game
        price = m.group(1)
        game = m.group(2)

        # Stores the listing as a dictionary in listings
        listing = {"email": email, "game": game, "price": price}
        listings.append(listing)

    return listings