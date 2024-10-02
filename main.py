# PSU Football Ticket Exchange Webscraper
# James Taddei
# 2024-10-01

from scraper import scrape_listings
from database import check_for_unsaved_listings, overwrite_saved_listings

# Scrapes listings from Onward State and saves new ones
listings = scrape_listings()
new_listings = check_for_unsaved_listings(listings)

# Add new listings to the database
overwrite_saved_listings(listings)