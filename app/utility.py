marketplaces = ["americanas", "amazon"]


def get_marketplace_index(url: str):
    for index, marketplace in enumerate(marketplaces):
        if marketplace in url:
            return index
    return 0
