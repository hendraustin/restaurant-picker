import math
import random
import argparse
import requests


def get_lat_lon() -> int:
    city = input("Please input your city: ")
    state = input("Please input your state: ")

    locations = requests.get(f"https://geocode.maps.co/search?q={city}+{state}")

    # Geocode passes multiple potential locations, but they place their best 'guesstimate' in the 0th index
    lat = locations.json()[0]["lat"]
    lon = locations.json()[0]["lon"]
    return lat, lon


# Yelp Fusion API has a max of 50 businesses per page that are always sorted in the same order
# So, we're choosing a random initial starting point (offset) to select a restaurant from
def get_random_offset_page(lat: int, lon: int, total: int) -> list:
    max_limit = 50
    restaurants = []

    random_offset = random.randrange(0, math.floor(total / max_limit) * max_limit)
    url = f"https://api.yelp.com/v3/businesses/search?term=restaurant&latitude={lat}&longitude={lon}&offset={random_offset}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer ",
    }

    req = requests.get(url=url, headers=headers)

    businesses = req.json()["businesses"]

    for restaurant in businesses:
        restaurants.append(restaurant["name"])

    return restaurants


def get_list_of_restaurants(lat: int, lon: int) -> int:
    url = f"https://api.yelp.com/v3/businesses/search?term=restaurant&latitude={lat}&longitude={lon}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer ",
    }
    r = requests.get(url=url, headers=headers)
    total = r.json()["total"]

    restaurants = get_random_offset_page(lat, lon, total)

    return restaurants


def get_random_restaurant(restaurants: list) -> str:
    lat, lon = get_lat_lon()

    restaurants = get_list_of_restaurants(lat, lon)

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

    print(f"The ORP has chosen: {get_random_restaurant(args)}!")


if __name__ == "__main__":
    main()
