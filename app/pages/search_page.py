import streamlit as st

from app.utility import marketplaces, get_marketplace_index, publish_on_queue


def page():
    st.markdown(
        """
        # Páginar busca
        **URL**: O link para a primeira página da busca.  
        *Comportamento é inesperado caso não seja a primeira página pois a paginação de cada marketplace pode variar.*  
        **Marketplace**: O marketplace o qual a página pertence.  
        """
    )

    url = st.text_input(
        label="URL", help="Exemplo: https://www.amazon.com.br/s?k=laser"
    )

    marketplace = st.selectbox(
        label="Marketplace",
        options=marketplaces,
        index=get_marketplace_index(url=url),
        help="Tentamos inferir quando você bota o URL mas podemos errar",
    )

    if st.button("Inserir na fila"):
        with st.spinner(text="Inserindo..."):
            publish_on_queue({
                "url": url,
                "marketplace": marketplace
            }, queue=f"{marketplace}_search")
        
        st.success(body="Inserido!")
