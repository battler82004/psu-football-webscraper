# Miscellaneous Utility Functions
# James Taddei
# 2024-10-08

POSSIBLE_KEYS = ["game", "email", "max_price"]

def filter_listings(listings, filter_args):
    """
    Removes listings that do not meet any inputted arguments. Currently only filters by game.
    """
    filtered_listings = []

    for listing in listings:
        game = filter_args.get("game")
        if (game): # Checks for a None that would be returned if there's no game
            if (listing["game"].lower() == game):
                filtered_listings.append(listing)

    return filtered_listings

def filter_listings_WIP(listings, filter_args):
    for key in filter_args.keys():
        match key:
            case "game":
                game = filter_args.get("game")
                def filter_func(l):
                    return l["game"] == game
                listings = filter(filter_func, listings)
            case "email":
                email = filter_args.get("email")
                def filter_func(l):
                    return l["email"] == email
                listings = filter(filter_func, listings)
            case "max_price":
                max_price = int(filter_args.get("max_price"))
                def filter_func(l):
                    return int(l["price"]) <= max_price
                listings = filter(filter_func, listings)
            case _: # No arguements
                pass

    return listings