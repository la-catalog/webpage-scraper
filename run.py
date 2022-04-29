import logging
import streamlit as st

from app.pages import sku_page, search_page

logging.getLogger("pika").setLevel(logging.WARNING)

pages = {
    "Inserir na SKU na fila": sku_page.page,
    "Inserir na página de busca na fila": search_page.page,
}

page = st.selectbox(label="Página", options=pages.keys())

pages[page]()
