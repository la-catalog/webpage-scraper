import streamlit as st
from rabbit_models.sku_scraper import Body

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

if st.button("Inserir na fila"):
    with st.spinner(text="Inserindo..."):
        queue = f"{marketplace}_sku"
        body = Body(urls=[url], marketplace=marketplace)
        body.metadata.source = "scraper-webpage"
        message = body.json(exclude_none=True)

        publish_on_queue(message=message, queue=queue)

    st.success(body="Inserido!")
