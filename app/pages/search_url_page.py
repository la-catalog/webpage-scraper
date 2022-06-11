import streamlit as st
from rabbit_models.search_scraper import Body

from app.utility import get_marketplace_index, marketplaces, publish_on_queue


def page():
    st.markdown(
        """
        # Inserir busca  
        A página da busca vai entrar na fila com prioridade máxima.  
        Qualquer SKU vindo desta busca também vai entrar com prioridade máxima.  
        """
    )

    url = st.text_input(
        label="URL da primeira página da busca",
        help="""
        Comportamento é inesperado caso não seja a primeira página  
        Exemplo: https://www.amazon.com.br/s?k=laser  
        """,
    )

    marketplace = st.selectbox(
        label="Marketplace",
        options=marketplaces,
        index=get_marketplace_index(url=url),
        help="""
        Tentamos inferir pelo URL mas podemos errar  
        """,
    )

    if st.button("Inserir na fila"):
        with st.spinner(text="Inserindo..."):
            queue = f"{marketplace}_search"
            body = Body(url=url, marketplace=marketplace)
            body.metadata.source = "scraper-webpage"
            message = body.json(exclude_none=True)

            publish_on_queue(message=message, queue=queue)

        st.success(body="Inserido!")
