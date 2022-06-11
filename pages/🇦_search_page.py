import streamlit as st
from rabbit_models.search_scraper import Body

from utility.marketplaces import marketplaces
from utility.rabbit import publish_on_queue

st.markdown(
    """
    # Inserir busca  
    A busca vai entrar na fila com prioridade máxima.  
    Qualquer SKU vindo desta busca também vai entrar com prioridade máxima.  
    """
)

url = st.text_input(label="Busca")
marketplace = st.selectbox(label="Marketplace", options=marketplaces)

if st.button("Inserir na fila"):
    with st.spinner(text="Inserindo..."):
        queue = f"{marketplace}_search"
        body = Body(url=url, marketplace=marketplace)
        body.metadata.source = "scraper-webpage"
        message = body.json(exclude_none=True)

        publish_on_queue(message=message, queue=queue)

    st.success(body="Inserido!")
