# PSU Football Ticket Exchange Webscraper
# James Taddei
# 2024-09-24

import requests
from bs4 import BeautifulSoup
import re
import json
from decode import decode_email

# Gets the updated webpage from Onward State and checks that the request was successful
res = requests.get("https://onwardstate.com/penn-state-football-student-ticket-exchange/")
assert res.status_code == 200 # non-200 status code indicates an error
print(res.status_code)

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
    email = decode_email(m.group(1)) # decrpyts the Cloudflare encoding

    # Finds the price and game (opponent)
    m = re.search(r"wants (.*) for a (.*) \(.*\) ticket.", l)
    assert m is not None # lines with valid emails should include a price and game
    price = m.group(1)
    game = m.group(2)

    # Stores the listing as a dictionary in listings
    listing = {"email": email, "game": game, "price": price}
    listings.append(listing)

saved_listings = set()

# Copies all (if any) saved listings to determine which listings are new
try:
    with open("listings.txt") as f:
        for line in f.readlines():
            saved_listings.add(line.strip())
except FileNotFoundError: # If there is no "listing.txt", then there just are no saved listings
    print("No saved listings")

# Loops through each listing and prints it as a new listing if it is not already in saved_listings
for l in listings:
    l = json.dumps(l, sort_keys=True) # dumps: dump string (takes dictionary and dumps it into a string)
    if (l not in saved_listings):
        print(l)

# Writes all of the data from listings into "listings.txt"
with open("listings.txt", "w") as f:
    serialized_listings = map(lambda l: f"{json.dumps(l, sort_keys=True)}\n", listings) # Converts to a str with new lines
    f.writelines(serialized_listings)