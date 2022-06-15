import os

MARKETPLACES = ["americanas", "amazon", "rihappy"]


def get_marketplace_index(url: str):
    for index, marketplace in enumerate(MARKETPLACES):
        if marketplace in url:
            return index
    return 0
