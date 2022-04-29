import streamlit as st

from marketplaces import marketplaces, get_marketplace_index


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
        print("insert on queue")