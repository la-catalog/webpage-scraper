import json
import os
import re
from datetime import timedelta

import streamlit as st
from bson.regex import Regex
from la_stopwatch import Stopwatch
from page_infra.options import get_marketplace_infra
from page_sku import SKU
from pymongo import MongoClient
from structlog.stdlib import get_logger
from webpage_components import (display_attributes, display_basic,
                                display_images, display_measurements,
                                display_prices, display_rating,
                                display_segments, display_weight, search_bar,
                                search_info_bar)

from utility.marketplaces import MARKETPLACES


def display_result(result: list, duration: timedelta) -> None:
    view_mode = search_info_bar(
        results_quantity=len(result),
        time_spent=f"{duration}",
    )

    for hit in result:
        with st.expander(label=hit["name"], expanded=True):
            match view_mode:
                case "default":
                    beautiful_hit(hit)
                case "json":
                    st.json(hit)
                case "code":
                    hit = json.dumps(hit, indent=2, ensure_ascii=False)
                    st.code(hit, language="json")


def beautiful_hit(hit: dict) -> None:
    sku = SKU(**hit)
    left_col, right_col = st.columns([2, 2])

    with right_col:
        for field, value in hit.items():
            if not isinstance(value, (dict, list)):
                display_basic(field=field, value=value)

    with left_col:
        display_images(images=sku.images)
        display_segments(segments=sku.segments)
        display_rating(
            min_value=sku.rating.min,
            max_value=sku.rating.max,
            current_value=sku.rating.current,
        )
        display_measurements(
            main_length=sku.measurement.length,
            main_width=sku.measurement.width,
            main_height=sku.measurement.height,
            main_unit=sku.measurement.unit,
            package_length=sku.package.length,
            package_width=sku.package.width,
            package_height=sku.package.height,
            package_unit=sku.package.unit,
        )
        display_weight(
            main_weight=sku.measurement.weight,
            main_weight_unit=sku.measurement.weight_unit,
            package_weight=sku.package.weight,
            package_weight_unit=sku.package.weight_unit,
        )
        display_prices([(p.value, p.currency) for p in sku.prices])

    display_attributes(
        attributes=[(a.name, a.value) for a in sku.attributes],
        id_=str(sku.id),
    )


st.set_page_config(layout="wide", page_icon="📕")

query, marketplace = search_bar(marketplaces=MARKETPLACES)

# Prepare query
query = re.escape(query)
pattern = re.compile(f"{query}", re.IGNORECASE)
regex = Regex.from_native(pattern)
regex.flags ^= re.UNICODE

# Get database information
infra = get_marketplace_infra(marketplace=marketplace, logger=get_logger())
database = infra.sku_database
collection = infra.sku_collection

# Execute query
stopwatch = Stopwatch()
client = MongoClient(os.environ["MONGO_URL"])
cursor = client[database][collection].find({"$or": [
    {"_id": regex},
    {"name": regex},
    {"description": regex},
]})
result = list(cursor)

display_result(result, stopwatch.duration())
