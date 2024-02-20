import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='logo.png'
)

st.write("# Home")

st.markdown( """---""" )

st.markdown(
    '''
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for help
        Contactar Raíssa Thibes no Discord 
        @raissa.thibes
    ''' 
)