#
# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    PRE-ÂMBULO DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Importar libraries
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from haversine import haversine  # para calcular a distância entre dois pontos geográficos

import os
os.add_dll_directory('C:\\Users\\HCInsula\\Miniconda\\DLLs')  # para dar certo as dependências

import streamlit as st   # to display things in Streamlit API

import folium                               # to things on maps
from streamlit_folium import folium_static  # to indeed show the map

from PIL import Image    # to bring images to show in StreamLit

from datetime import datetime  # to work with dates and times

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
    df1 = df1.loc[ df1['Delivery_person_Age'] != 'NaN '    , : ]
    df1 = df1.loc[ df1['Delivery_person_Ratings'] != 'NaN ', : ]
    df1 = df1.loc[ df1['multiple_deliveries'] != 'NaN '    , : ]
    #df1 = df1.loc[ df1['Time_Orderd'] != 'NaN '           , : ]  # Time_Order_picked
    #df1 = df1.loc[ df1['Time_Order_picked'] != 'NaN '     , : ]
    df1 = df1.astype({'multiple_deliveries':'str'})
    df1 = df1.loc[ df1['multiple_deliveries'] != 'nan', : ]
    df1 = df1.loc[ df1['Road_traffic_density'] != 'NaN '   , : ]
    df1 = df1.loc[ df1['City'] != 'NaN '      , : ]
    df1 = df1.loc[ df1['Festival'] != 'NaN '      , : ]
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
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Carregar os dados da tabela
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
df = pd.read_csv('train.csv')
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
st.header( 'Marketplace - Visão Entregadores' )
#
# # # st.dataframe( df )                        #  . . . # Shows the dateframe df
#
# Sidebar 1
image_path = 'logo.png'
image = Image.open( image_path )
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
    ['Low','Medium','High','Jam']
)
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
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Visualizações das análises
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
tab1, tab2, tab3 = st.tabs( ['Visão Geral', '_', '_'] )
#
with tab1:
    with st.container():
        st.title( 'Métricas Gerais' )
        #
        col1, col2, col3, col4 = st.columns( 4, gap='large' )
        with col1:
            # Maior Idade dos entregadores
            maior_idade = df1.loc[ :, 'Delivery_person_Age' ].max()
            col1.metric( 'Maior Idade', maior_idade)
        with col2:
            # Menor Idade dos entregadores
            menor_idade = df1.loc[ :, 'Delivery_person_Age' ].min()
            col2.metric( 'Menor Idade', menor_idade)
        with col3:
            # Melhor condição dos veículos
            melhor_condicao = df1.loc[ :, 'Vehicle_condition' ].max()
            col3.metric( 'Melhor condição', melhor_condicao)
        with col4:
            # Pior condição dos veículos
            pior_condicao = df1.loc[ :, 'Vehicle_condition' ].min()
            col4.metric( 'Pior condição', pior_condicao)
            #
    with st.container():
        st.markdown( """---""" )
        st.title( 'Avaliações' )
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown( "#### Avaliação média por Entregador" )
            df_avg_ratings_per_deliver = ( df1.loc[ :, ['Delivery_person_ID', 'Delivery_person_Ratings'] ]
                                              .groupby( ['Delivery_person_ID'] )
                                              .mean()
                                              .reset_index()
                                          )
            st.dataframe( df_avg_ratings_per_deliver )
            #
        with col2:
            st.markdown( '#### Avaliações médias por trânsito' )
            df_avg_std_ratting_by_traffic = ( df1.loc[ :, ['Delivery_person_Ratings','Road_traffic_density']]
                                                 .groupby( ['Road_traffic_density'] )
                                                 .agg( {'Delivery_person_Ratings':['mean','std']} )
                                            )
            # definir colunas
            df_avg_std_ratting_by_traffic.columns = ['deliveryRate_mean','deliveryRate_std']
            # reset index
            df_avg_std_ratting_by_traffic = df_avg_std_ratting_by_traffic.reset_index()
            #
            st.dataframe( df_avg_std_ratting_by_traffic )
            #
            st.markdown( '#### Avaliações médias por clima' )
            df_avg_std_ratting_by_weather = ( df1.loc[ :, ['Delivery_person_Ratings','Weatherconditions']]
                                                 .groupby( ['Weatherconditions'] )
                                                 .agg( {'Delivery_person_Ratings':['mean','std']} )
                                            )
            # definir colunas
            df_avg_std_ratting_by_weather.columns = ['deliveryRate_mean','deliveryRate_std']
            # reset index
            df_avg_std_ratting_by_weather = df_avg_std_ratting_by_weather.reset_index()
            #
            st.dataframe( df_avg_std_ratting_by_weather )
        with st.container():
            st.markdown( """---""" )
            st.title( "Velocidade de Entrega" )
            col1,col2 = st.columns( 2 )
            with col1:
                st.markdown( "Entregadores mais rápidos" )
                st.markdown( "por cidade" )
                df2 = ( df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
                           .groupby( ['City','Delivery_person_ID'] )
                           .mean()
                           .sort_values( ['City','Time_taken(min)'] , ascending=True )
                           .reset_index()
                      )
                # Selecionar os melhores 10 de cada cidade
                df3_aux1 =  df2.loc[ df2['City']=='Metropolitian', :].head( 10 )
                df3_aux2 =  df2.loc[ df2['City']=='Urban'        , :].head( 10 )
                df3_aux3 =  df2.loc[ df2['City']=='Semi-Urban'   , :].head( 10 )
                df3 = pd.concat( [ df3_aux1 , df3_aux2 , df3_aux3   ]).reset_index( drop=True )
                st.dataframe( df3 )
            with col2:
                st.markdown( "Entregadores mais lentos" )
                st.markdown( "por cidade" )
                df2 = ( df1.loc[ :, ['Delivery_person_ID','City','Time_taken(min)'] ]
                           .groupby( ['City','Delivery_person_ID'] )
                           .mean()
                           .sort_values( ['City','Time_taken(min)'] , ascending=False )
                           .reset_index()
                      )
                # Selecionar os 10 mais lento de cada cidadede cada cidade
                df3_aux1 =  df2.loc[ df2['City']=='Metropolitian', :].head( 10 )
                df3_aux2 =  df2.loc[ df2['City']=='Urban'        , :].head( 10 )
                df3_aux3 =  df2.loc[ df2['City']=='Semi-Urban'   , :].head( 10 )
                df3 = pd.concat( [ df3_aux1 , df3_aux2 , df3_aux3   ]).reset_index( drop=True )
                st.dataframe( df3 )