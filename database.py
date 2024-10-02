# Database Interactions
# James Taddei
# 2024-10-01

import json

def serialized_listing(listing):
    """
    Serializes the inputted dictionary (listing) into a JSON formatted string.
    """
    return json.dumps(listing, sort_keys=True)

def unserialize_line(line):
    """
    Unserializes the inputted JSON formatted string (line) into a dictionary (listing).
    """
    return json.loads(line)

def _read_database():
    """
    Reads and returns all data from the database as a list of JSON formatted strings.
    """
    lines = []

    # Copies all (if any) saved listings to determine which listings are new
    try:
        with open("listings.txt") as f:
            for line in f.readlines():
                lines.append(line.strip())
    except FileNotFoundError: # If there is no "listing.txt", then there just are no saved listings
        pass

    return lines

def get_saved_listings():
    """
    Returns a list of all saved listings in a dictionary format.
    """
    saved_lines = _read_database()
    saved_listings = map(unserialize_line, saved_lines) # JSON formatted string to dictionary
    return saved_listings

def check_for_unsaved_listings(listings):
    """
    Returns all unsaved listings in the form of a JSON formatted string (listing).
    """
    # Get data from database and convert it into a set
    saved_lines = _read_database()
    saved_lines = set(saved_lines)

    unsaved_listings = []

    # Loops through each listing and adds it to unsaved_listings if it is not already in saved_lines
    for listing in listings:
        line = serialized_listing(listing)
        if  (line not in saved_lines):
            unsaved_listings.append(line)

    return unsaved_listings

def overwrite_saved_listings(listings):
    """
    Adds all data listings to the database.
    """
    # Formats listings as JSON formatted strings (lines)
    listings = map(lambda l: f"{serialized_listing(l)}\n", listings)
    # Writes all of the data from listings into "listings.txt"
    with open("listings.txt", "w") as f:
        f.writelines(listings)