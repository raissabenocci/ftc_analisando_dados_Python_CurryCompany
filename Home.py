# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Importar libraries
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
import streamlit as st
from PIL import Image
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Configurar página com ícone e barra lateral
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
st.set_page_config(
    page_title='Home',
    page_icon='🎲'   )
#
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Sidebar
#
# image_path = (  )           # r'/Users/HCInsula/Documents/DataScience_Studies/ComunidadeDS/repos/ftc_analisando_dados_python/CurryCompany_app/'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( 'Fastest delivery in town' )
st.sidebar.markdown( """---""" )
#
#
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Texto da página
# 
st.write( "Curry Company Growth Dashboard" )
#
# st.markdown(
#     """
#     Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
#     ### Como utilizar esse Growth Dashboard?
#     - Visão da Empresa Curry:
#         - Visão Gerencial - métricas gerais de comportamento
#         - Visão Tática - indicadores semanais de crescimento
#         - Visão Geográfica - insights de geolocalização
#     - Visão dos Entregadores:
#         - Acompanhamento dos indicadores semanais de crescimento
#     - Visão dos Restaurantes:
#         - Indicadores semanais de crescimento dos restaurantes
#      a# Ask for help
#     - Raíssa Thibes
#         - raissabenoccit@gmail.com
#     """
# )
#
st.markdown( """---""" )
st.markdown( 'Powered by CDS & Raíssa Thibes' )