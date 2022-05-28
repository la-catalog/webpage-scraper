import streamlit as st
from rabbit_models.sku_scraper import Body

from app.utility import get_marketplace_index, marketplaces, publish_on_queue


def page():
    st.markdown(
        """
        # Scrapear SKU
        **URL**: O link para a página do SKU.  
        **Marketplace**: O marketplace o qual o SKU pertence.  
        """
    )

    url = st.text_input(
        label="URL", help="Exemplo: https://www.amazon.com.br/dp/B074WTM8PH"
    )

    marketplace = st.selectbox(
        label="Marketplace",
        options=marketplaces,
        index=get_marketplace_index(url=url),
        help="Tentamos inferir quando você bota o URL mas podemos errar",
    )

    if st.button("Inserir na fila"):
        with st.spinner(text="Inserindo..."):
            queue = f"{marketplace}_sku"
            body = Body(urls=[url], marketplace=marketplace)
            body.metadata.source = "scraper-webpage"
            message = body.json(exclude_none=True)

            publish_on_queue(message=message, queue=queue)

        st.success(body="Inserido!")
