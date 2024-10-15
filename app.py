# Webapp for the Ticket Scraper
# James Taddei
# 2024-10-08

import flask
from scraper import scrape_listings
from errors import ScrapingError
from utils import filter_listings
from database import check_for_unsaved_listings, overwrite_saved_listings

app = flask.Flask(__name__)

@app.route("/")
def index():
    # Scrapes listings
    try:
        listings = scrape_listings()
    except ScrapingError:
        return "No data", 500

    # Filters listings based on the inputted arguments
    args = flask.request.args
    if (len(args.keys()) > 0):
        listings = filter_listings(listings, args)

    # Formats and returns the final listings
    res = {"listings": listings}
    return res, 200

@app.route("/update", methods=["POST"])
def update():
    # Scrapes listings
    try:
        listings = scrape_listings()
    except ScrapingError:
        return "No data", 500
    
    unsaved_listings = check_for_unsaved_listings(listings)
    overwrite_saved_listings(listings) # adds new listings

    # Formats and returns the final listings
    res = {"listings": listings}
    return res, 200