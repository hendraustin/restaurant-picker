import sys
import math
import random
import argparse
import requests


def get_location() -> str:
    city = input("Please input your city: ")
    state = input("Please input your state: ")
    return (city + " " + state).replace(" ", "%")


# Yelp Fusion API has a max of 50 businesses per page that are always sorted in the same order
# So, we're choosing a random initial starting point (offset) to select a restaurant from
def get_random_offset_page(location: str, total: int) -> list:
    max_limit = 50
    max_businesses_per_request = 1000
    restaurants = []

    if total < max_businesses_per_request:
        random_offset = random.randrange(0, math.floor(total / max_limit) * max_limit)
    else:
        random_offset = random.randrange(0, max_businesses_per_request - 1)

    url = f"https://api.yelp.com/v3/businesses/search?term=restaurant&location={location}&offset={random_offset}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer ",  # API key goes here
    }

    req = requests.get(url=url, headers=headers)

    businesses = req.json()["businesses"]

    for restaurant in businesses:
        restaurants.append(restaurant["name"])

    return restaurants


def get_list_of_restaurants(location: str) -> int:
    url = (
        f"https://api.yelp.com/v3/businesses/search?term=restaurant&location={location}"
    )
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer ",  # API key goes here
    }
    r = requests.get(url=url, headers=headers)

    try:
        total = r.json()["total"]
    except KeyError:
        sys.exit(
            "No restaurants found, check the city and state are correct for the ORP to facilitate your culinary venture."
        )

    restaurants = get_random_offset_page(location, total)

    return restaurants


def get_random_restaurant() -> str:
    location = get_location()

    restaurants = get_list_of_restaurants(location)

    return random.choice(restaurants)


# WIP: Update to utilize kwargs(?)
def main():
    parser = argparse.ArgumentParser(description="Select a random restaurant")
    parser.add_argument(
        "--healthy",
        help="Boolean to filter by healthy options",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--sitdown",
        help="Boolean to filter by healthy options",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    print(f"The ORP has chosen: {get_random_restaurant()}!")


if __name__ == "__main__":
    main()
