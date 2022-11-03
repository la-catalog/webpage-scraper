import streamlit as st
from page_infra.options import get_marketplace_infra
from rabbit_models.search_scraper import Body, Metadata
from structlog.stdlib import get_logger

from utility.marketplaces import MARKETPLACES, get_marketplace_index
from utility.rabbit import publish_on_queue

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
    options=MARKETPLACES,
    index=get_marketplace_index(url=url),
    help="""
    Tentamos inferir pelo URL mas podemos errar  
    """,
)

infra = get_marketplace_infra(
    marketplace=marketplace,
    logger=get_logger(),
)

if st.button("Inserir na fila"):
    with st.spinner(text="Inserindo..."):
        message = Body(
            url=url,
            marketplace=marketplace,
            metadata=Metadata(
                source="webpage",
            ),
        ).json(exclude_none=True)

        publish_on_queue(message=message, queue=infra.search_queue)

    st.success(body="Inserido!")
