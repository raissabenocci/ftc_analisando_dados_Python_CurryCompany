# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    PRE-ÂMBULO DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Importar libraries
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
#
from haversine import haversine  # para calcular a distância entre dois pontos geográficos
#
import os
#os.add_dll_directory('C:\\Users\\HCInsula\\Miniconda\\DLLs')  # para dar certo as dependências
from os.path import exists
#
import streamlit as st   # to display things in Streamlit API
#
import folium                               # to things on maps
from streamlit_folium import folium_static  # to indeed show the map
#
from PIL import Image    # to bring images to show in StreamLit
#
from datetime import datetime  # to work with dates and times
#
#
# Page settings
st.set_page_config(
    page_title='Visão empresa',
    page_icon='icons/company.png',
    layout='wide'
)
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Funções
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Limpar  o dataframe principal
def clean_data( df1 ):
    """ FUNÇÃO que aplica todas as limpezas e transformações de tipos de variáveis sobre o dataframe df1 e o retorna

        Tipos de limpeza:
        1. Remoção de NaN
        2. Tipos de variáveis
        3. Remoção de espaços extras
        4. Formatação de datas
        5. Limpeza da coluna de tempo (remoção do texto (min) da variável numérica Time_taken(min)
        6. Definição da coluna com a semana do ano a que cada data se refere
      
        Input:  Dataframe
        Output: Dataframe
    """
    #
    # Jogar fora linhas com 'NaN'
    df1 = df1.loc[ df1['Delivery_person_Age']     != 'NaN ' , : ]
    df1 = df1.loc[ df1['Delivery_person_Ratings'] != 'NaN ' , : ]
    df1 = df1.loc[ df1['multiple_deliveries']     != 'NaN ' , : ]
    df1 = df1.astype( { 'multiple_deliveries':'str' } )
    df1 = df1.loc[ df1['multiple_deliveries']     != 'nan'  , : ]
    df1 = df1.loc[ df1['Road_traffic_density']    != 'NaN ' , : ]
    df1 = df1.loc[ df1['City']                    != 'NaN ' , : ]
    df1 = df1.loc[ df1['Festival']                != 'NaN ' , : ]
    # df1 = df1.loc[ df1['Time_Orderd']           != 'NaN ' , : ]  # Time_Order_picked
    # df1 = df1.loc[ df1['Time_Order_picked']     != 'NaN ' , : ]
    #
    #
    # Converter de object para tipos apropriados
    df1 = df1.astype({'Delivery_person_Age':'int64',
                      'Delivery_person_Ratings':'float64',
                      'multiple_deliveries':'int64',
                      'Vehicle_condition':'int64'})
    #
    # converter a "Order Date" para datetime
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y')
    # df1['Time_Orderd'] = pd.to_datetime( df1['Time_Orderd'], format='%H:%M:%S')
    # df1['Time_Order_picked'] = pd.to_datetime( df1['Time_Order_picked'], format='%H:%M:%S')
    #
    #
    # Tirar espaços que sobram
    df1.loc[:, ['ID']]                   = df1.loc[:, ['ID']                   ].squeeze().str.strip()
    df1.loc[:, ['Delivery_person_ID']]   = df1.loc[:, ['Delivery_person_ID']   ].squeeze().str.strip()
    df1.loc[:, ['Road_traffic_density']] = df1.loc[:, ['Road_traffic_density'] ].squeeze().str.strip()
    df1.loc[:, ['Type_of_order']]        = df1.loc[:, ['Type_of_order']        ].squeeze().str.strip()
    df1.loc[:, ['Type_of_vehicle']]      = df1.loc[:, ['Type_of_vehicle']      ].squeeze().str.strip()
    df1.loc[:, ['City']]                 = df1.loc[:, ['City']                 ].squeeze().str.strip()
    df1.loc[:, ['Festival']]             = df1.loc[:, ['Festival']             ].squeeze().str.strip()
    #
    # Throw away the substring 'conditions ' from field ['Weatherconditions']
    # and '(min) ' from field ['Time_taken(min)']
    df1 = df1.replace({'Weatherconditions': 'conditions ','Time_taken(min)': r"\(.*\) "},                   {'Weatherconditions': '','Time_taken(min)': ""}, regex=True)
    # or  df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    #
    df1 = df1.astype({'Time_taken(min)':'int64'})
    #
    # Definir a qual semana do ano cada data se refere
    df1.loc[:, ['week_of_year']]         = df1.loc[:,'Order_Date'].dt.strftime('%U') # Colocando %W usa a segunda-feira como o primeiro dia da semana; %U é domingo
    #
    return df1
#
#
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Plot  Bar chart
def barplot_OrdersByDay_count( df1 ):
    cols = ['ID','Order_Date']
    df_aux = df1.loc[ : , cols].groupby( ['Order_Date'] ).count().reset_index()
    fig = px.bar( df_aux, x='Order_Date', y='ID')
    return fig
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Plot  Pie chart
def pieplot_CityDlivrAg_avg( df1 ):
    """ FUNÇÃO plot pie chart com a média de idade dos entregadores para cada cidade
        Input:   Dataframe
        Output:  fig com px.pie
    """
    #
    cols = ['Delivery_person_Age','City']
    df_aux = df1.loc[ : , cols ].groupby( ['City'] ).mean().reset_index()
    fig = px.pie( df_aux, values='Delivery_person_Age', names='City')
    return fig
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Plot  Scatter chart
def scatterplot_CityTrafficDlivrs_count( df1 ):
    """ FUNÇÃO com scatter plot com a quantidade de entregadores por tipo de tráfego
        Agregação é feita por dia
        Inputs: Dataframe      
        Output: fig com px.scatter
    """
    #
    cols = ['ID','Road_traffic_density','City']
    df_aux = df1.loc[ ( df1['Road_traffic_density'] != 'NaN') & ( df1['City'] != 'NaN') , cols ]
    df_aux = df_aux.groupby( ['Road_traffic_density','City'] ).count().reset_index()
    fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Plot  Line chart
def lineplot_DlivrsWeek_count( df1 ):
    """ FUNÇÃO plot line chart com quantidade de entregadores para semana
        Input:   Dataframe
        Output:  fig com px.line
    """
    #
    cols = ['ID','week_of_year']
    df_aux = df1.loc[ :, cols ].groupby( ['week_of_year'] ).count().reset_index()
    fig = px.line( df_aux , x='week_of_year' , y='ID')
    return fig
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Plot  Bar chart
def barplot_DlivrsScoreWeek_count( df1 ):
    """ FUNÇÃO plot bar chart com score médio de avaliação dos entregadores para semana
        Input:   Dataframe
        Output:  fig com px.line
    """
    #
    cols = ['Delivery_person_Ratings', 'week_of_year']
    df_aux = df1.loc[ :, cols ].groupby( ['week_of_year'] ).mean().reset_index()
    fig = px.bar( df_aux , x='week_of_year' , y='Delivery_person_Ratings')
    fig.update_xaxes( type='category' )
    fig.update_yaxes( range=(4.6, 4.66), constrain='domain' )
    return fig
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Plot   Map chart  com folium
def map_visao_geografica_restaurantes( df1 ):
    """ FUNÇÃO que cria a variável map contendo as coordenadas com as medianas da posição geográfica dos restaurante
        Agregação feita por cidade e tipo de tráfego
        Input:  Dataframe
        Output: map
    """
    #
    # Selecionar colunas
    cols1 = [ 'City','Road_traffic_density',    # 'City' é a região da cidade
              'Restaurant_latitude', 'Restaurant_longitude' ]
    cols2 = [ 'City','Road_traffic_density',    # 'City' é a região da cidade
              'Delivery_location_latitude', 'Delivery_location_longitude' ]
    #
    df_aux1 = df1.loc[ :, cols1] # para Locais dos Restaurantes
    df_aux2 = df1.loc[ :, cols2] # para Locais de Entrega
    #
    # Locais dos Restaurantes       -  mediana das latitudes e das longitudes
    df_aux1 = df_aux1.groupby( ['City','Road_traffic_density'] ).median().reset_index()
    #
    # Locais de Entrega (Delivery)  -  mediana das latitudes e das longitudes
    df_aux2 = df_aux2.groupby( ['City','Road_traffic_density'] ).median().reset_index()
    #
    # # PLOTAR O MAPA
    map = folium.Map()
    #
    # Para Locais de Entrega
    for index, location_info in df_aux2.iterrows():
      folium.Marker( [ location_info['Delivery_location_latitude'] , location_info['Delivery_location_longitude'] ],
                     popup=location_info[['City','Road_traffic_density']]
                    ).add_to( map )
    return map
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Carregar os dados da tabela
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
df = pd.read_csv( 'dataset/train.csv' )
df1 = df.copy()
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aviso do horário de execução do .py
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
print( 'Current time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print( "Possui ", len( df1 ) , "entregas na base\n" )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Limpeza de dados
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
df1 = clean_data( df1 )
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Layout de visão no StreamLit para dashboards
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Header 1
st.header( 'Marketplace - Visão Cliente' )
#
# # # st.dataframe( df )                        #  . . . # Shows the dateframe df
#
# Sidebar 1
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( 'Fastest delivery in town' )
st.sidebar.markdown( """---""" )
#
# # filtros do sidebar
st.sidebar.markdown( '### Filtros' )
#
date_slider = st.sidebar.slider(
    'Selecione a data limite',
    value=    df1['Order_Date'].min().to_pydatetime() + (df1['Order_Date'].max().to_pydatetime()-df1['Order_Date'].min().to_pydatetime()) / 2,  #  Standard date
    # value=    df1['Order_Date'].max().to_pydatetime() - datetime.timedelta(days=10),    # alternative to Standard date
    min_value=df1['Order_Date'].min().to_pydatetime() ,
    max_value=df1['Order_Date'].max().to_pydatetime() ,
    format='DD-MM-YYYY'
)
#
st.sidebar.markdown( """---""" )
trafficOptions = st.sidebar.multiselect(
    'Selecione as condições de trânsito',
    ['Low','Medium','High','Jam'],
    ['Low','High'])
#
#
# # fechamento do sidebar
st.sidebar.markdown( """---""" )
st.sidebar.markdown( 'Powered by CDS - Raíssa Thibes' )
#
#
# # Header 2
# st.header( f"Data selecionada:  {date_slider.date()}",   divider='rainbow' )  #  prints the selected value in the slider as a date (doesn't show the time) and draws a rainbow line underneath the text
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aplicação de filtros
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[ linhas_selecionadas, :]
#
# Filtro de condição de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( trafficOptions )
df1 = df1.loc[ linhas_selecionadas, :]
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Visualizações das análises
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  Visão Gerencial
with tab1: # Quantidade de pedidos por dia
    with st.container():
        st.markdown( '## Pedidos por dia' )
        fig = barplot_OrdersByDay_count( df1 )
        st.plotly_chart( fig, use_container_width=True )
    with st.container():
        col1, col2 = st.columns( 2 )                    # quebrado em 2 colunas
        with col1:
            st.markdown( '### Entregadores por cidade' )
            fig = pieplot_CityDlivrAg_avg( df1 )
            st.plotly_chart( fig, use_container_width=True)            
        with col2:
            st.markdown( '### Entregadores por cidade e tráfego' )
            fig = scatterplot_CityTrafficDlivrs_count( df1 )
            st.plotly_chart( fig, use_container_width=True )
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #   Visão Tática
with tab2:
    st.markdown( '### Por semana' )
    with st.container(): # Quantidade de pedidos por semana.
        fig = lineplot_DlivrsWeek_count( df1 )
        st.plotly_chart( fig , use_container_width=True )
    with st.container():  # Gráfico de barras, mostrando as avaliações médias das entregas por semana.
        fig = barplot_DlivrsScoreWeek_count( df1 )
        st.plotly_chart( fig , use_container_width=True )
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #   Visão Geográfica
with tab3:
    st.markdown( '# Mapas' )
    map = map_visao_geografica_restaurantes( df1 )
    folium_static( map, width=1024, height=600 )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 