import random
import argparse

from restaurants import restaurants


def get_random_restaurant(args: list) -> str:
    restaurants_list = []

    for restaurant in restaurants:
        if args.healthy is False and args.sitdown is False:
            restaurants_list.append(restaurant["Name"])
        elif (args.healthy is True and args.healthy == restaurant["Healthy"]) and (
            args.sitdown is True and args.sitdown == restaurant["Sit down"]
        ):
            restaurants_list.append(restaurant["Name"])
        elif (
            args.healthy is True
            and args.healthy == restaurant["Healthy"]
            and args.sitdown is False
        ):
            restaurants_list.append(restaurant["Name"])
        elif (
            args.sitdown is True
            and args.sitdown == restaurant["Sit down"]
            and args.healthy is False
        ):
            restaurants_list.append(restaurant["Name"])

    return random.choice(restaurants_list)


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
