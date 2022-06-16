from page_infra.options import options as marketplaces

MARKETPLACES = marketplaces.keys()


def get_marketplace_index(url: str):
    for index, marketplace in enumerate(MARKETPLACES):
        if marketplace in url:
            return index
    return 0
