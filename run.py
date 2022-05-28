import logging

import streamlit as st

from app.pages import search_page, sku_page

logging.getLogger("pika").setLevel(logging.WARNING)

pages = {
    "Inserir SKU na fila": sku_page.page,
    "Inserir página de busca na fila": search_page.page,
}

page = st.selectbox(label="Página", options=pages.keys())

pages[page]()
