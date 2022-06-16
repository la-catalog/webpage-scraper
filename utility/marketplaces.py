from page_infra.options import options as marketplaces


def get_marketplace_index(url: str):
    for index, marketplace in enumerate(marketplaces.keys()):
        if marketplace in url:
            return index
    return 0
