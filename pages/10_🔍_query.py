import os
import re
from datetime import datetime

import streamlit as st
from bson.regex import Regex
from page_infra.options import get_marketplace_infra
from page_models import Query
from pymongo import MongoClient
from pymongo.collection import Collection
from streamlit.delta_generator import DeltaGenerator
from structlog.stdlib import get_logger
from webpage_components import search_bar

from utility.marketplaces import MARKETPLACES


def execute_query(query_start: str, marketplace: str) -> tuple[int, list[str]]:
    # Prepare query
    query_start = re.escape(query_start)
    pattern = re.compile(f"^{query_start}", re.IGNORECASE)
    regex = Regex.from_native(pattern)
    regex.flags ^= re.UNICODE

    # Get database information
    infra = get_marketplace_infra(marketplace=marketplace, logger=get_logger())
    database = infra.search_database
    collection = infra.search_collection

    # Execute query
    client = MongoClient(os.environ["MONGO_URL"])
    yield client[database][collection].count_documents({"query": regex}),
    yield list(
        d["query"]
        for d in client[database][collection].find(
            {"query": regex},
            {"_id": 0, "query": 1},
            sort=[("query", 1)],
            limit=100,
        )
    )


def add_query(query: str, marketplace: str) -> None:
    # Get database information
    infra = get_marketplace_infra(marketplace=marketplace, logger=get_logger())
    database = infra.search_database
    collection = infra.search_collection

    # Execute query
    client = MongoClient(os.environ["MONGO_URL"])
    client[database][collection].insert_one(
        document=Query(query=query).dict(),
    )


st.set_page_config(layout="wide", page_icon="📕")

query_start, marketplace = search_bar(
    marketplaces=MARKETPLACES,
    search_label="Apenas queries começando com...",
)

count, queries = execute_query(
    query_start=query_start,
    marketplace=marketplace,
)

st.json(body=queries, expanded=True)

new_query = st.text_input(
    label="Inserir nova query na lista",
    help="Queries vão ser sempre caixa baixa",
)

if st.button(label="➕"):
    with st.spinner(text="Inserindo..."):
        add_query(query=new_query, marketplace=marketplace)
        st.experimental_rerun()
