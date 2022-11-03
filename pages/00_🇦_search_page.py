import streamlit as st
from page_infra.options import get_marketplace_infra
from rabbit_models.search_scraper import Body, Metadata
from structlog.stdlib import get_logger

from utility.marketplaces import MARKETPLACES
from utility.rabbit import publish_on_queue

st.markdown(
    """
    # Inserir busca  
    A busca vai entrar na fila com prioridade máxima.  
    Qualquer SKU vindo desta busca também vai entrar com prioridade máxima.  
    """
)

url = st.text_input(label="Busca")
marketplace = st.selectbox(label="Marketplace", options=MARKETPLACES)
infra = get_marketplace_infra(marketplace=marketplace, logger=get_logger())

if st.button("Inserir na fila"):
    with st.spinner(text="Inserindo..."):
        body = Body(
            url=url, marketplace=marketplace, metadata=Metadata(source="webpage")
        )
        body.metadata.source = "scraper-webpage"
        message = body.json(exclude_none=True)

        publish_on_queue(message=message, queue=infra.search_queue)

    st.success(body="Inserido!")
