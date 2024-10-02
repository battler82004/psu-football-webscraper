# Webapp for the Ticket Scraper
# James Taddei
# 2024-10-01

import flask
from scraper import scrape_listings
from errors import ScrapingError

app = flask.Flask(__name__)

@app.route("/")
def index():
    flask.request.args
    try:
        listings = scrape_listings()
        res = {"listings": listings}
        return res, 200
    except ScrapingError:
        return "No data", 500