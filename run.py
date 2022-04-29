import streamlit as st

from pages import sku_page, search_page

pages = {
    "Inserir na SKU na fila": sku_page.page,
    "Inserir na página de busca na fila": search_page.page,
}



page = st.selectbox(label="Página", options=pages.keys())

pages[page]()

