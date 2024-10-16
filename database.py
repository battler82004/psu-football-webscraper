# Database Interactions
# James Taddei
# 2024-10-16

import sqlite3

DATABASE_FILE = "listings.db"

def get_saved_listings():
    """
    Returns a list of all saved listings in a dictionary format.
    """
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()

    query = "SELECT * FROM listings;"
    res = cursor.execute(query)
    db.close()
    return res.fetchall()

def check_for_unsaved_listings(listings):
    """
    Returns a list of all unsaved listings in a dictionary format.
    """
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()

    unsaved_listings = []
    query = "SELECT * FROM listings WHERE game = ? AND email = ? AND price = ?;"

    for listing in listings:
        res = cursor.execute(query, (listing["game"], listing["email"], listing["price"]))
        if (res.fetchone() is None):
            unsaved_listings.append(listing)
    
    return unsaved_listings

def overwrite_saved_listings(listings):
    """
    Adds all data listings to the database.
    """
    _reset_db()
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()

    query = "INSERT INTO listings (game, email, price) VALUES (?, ?, ?);"

    for listing in listings:
        cursor.execute(query, (listing["game"], listing["email"], listing["price"]))
    
    db.commit()
    db.close()

def _reset_db():
    """
    Reset (drop and recreate) the database.
    """
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()

    query = "DROP TABLE IF EXISTS listings;"
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            email TEXT NOT NULL,
            price REAL NOT NULL
        )
    """
    cursor.execute(query)
    db.commit()
    db.close()

if (__name__ == "__main__"):
    _reset_db()