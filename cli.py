import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        description="Budget System Tracker CLI"
    )

    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="User name"
    )

    parser.add_argument(
        "--income",
        type=float,
        required=True,
        help="Monthly income"
    )

    parser.add_argument(
        "--tax",
        choices=["flat", "progressive"],
        default="flat",
        help="Tax strategy type"
    )

    return parser