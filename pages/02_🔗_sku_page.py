import streamlit as st
from page_infra.options import get_marketplace_infra
from rabbit_models.page_scraper import Body
from structlog.stdlib import get_logger

from utility.marketplaces import MARKETPLACES, get_marketplace_index
from utility.rabbit import publish_on_queue

st.markdown(
    """
    # Inserir SKU  
    O SKU vai entrar na fila com prioridade máxima.  
    """
)

url = st.text_input(
    label="URL para a página do SKU",
    help="""
    Exemplo: https://www.amazon.com.br/dp/B074WTM8PH  
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
        body = Body(urls=[url], marketplace=marketplace)
        body.metadata.source = "scraper-webpage"
        message = body.json(exclude_none=True)

        publish_on_queue(message=message, queue=infra.sku_queue)

    st.success(body="Inserido!")
