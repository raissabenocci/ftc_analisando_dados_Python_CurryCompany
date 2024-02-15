#
# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    PRE-ÂMBULO DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#  Importar libraries
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
#
from haversine import haversine  # para calcular a distância entre dois pontos geográficos
#
import os
os.add_dll_directory('C:\\Users\\HCInsula\\Miniconda\\DLLs')  # para dar certo as dependências
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
    page_title='Visão restaurantes',
    # page_icon='favicon.ico',
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
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função para calcular a distância usando a biblioteca haversine
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def haversine_distance(row):
    restaurante_coords = (row['Restaurant_latitude'],        row['Restaurant_longitude'])
    entrega_coords     = (row['Delivery_location_latitude'], row['Delivery_location_longitude'])

    # A função haversine retorna a distância em quilômetros
    distance = haversine( restaurante_coords, entrega_coords )

    return distance
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função para calcular a distância aplicando a função haversine_distance
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def distanciaMedia( df1, cols):
    """ FUNÇÃO que calcula pelo método haversine a distância média entre o restaurante e o local de entrega
        Input: dataframe df1 e nome das colunas cols
        Output: distância média
    """
    df_aux = df1.loc[ :, cols].copy()
    
    # Cria uma nova coluna 'distancia_haversine' com as distâncias calculadas usando a função haversine_distance
    df_aux['distancia_haversine'] = df_aux.apply(lambda row: haversine_distance(row) , axis=1)   # usa a função criada acima
    distMedia = df_aux['distancia_haversine'].mean()
    return distMedia
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função para calcular tempo médio ou desvio padrão no Festival ou não
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def tempoFestival_avg_std( df1, yn_Festival, type_metric):
    """ FUNÇÃO calcula o tempo médio ou o desvio padrão do tempo de entrega, quando em Festival ou não
    
        Input:  df1          dataframe
                cols         colunas
                yn_Festival  'Yes' ou 'No'
                type_metric  'avg' ou 'std'
        Output: metricaTime com tempo médio 'avg_time'  ou desvio padrão do tempo 'std_time'
    """
    cols = [ 'Time_taken(min)', 'Festival' ]
    df_aux = df1.loc[:,cols].copy()
    df_aux = df_aux.groupby( [ 'Festival' ] ).agg( {'Time_taken(min)':['mean','std']} )
    df_aux.columns = [ 'avg_time', 'std_time' ]
    df_aux = df_aux.reset_index()
    
    if type_metric=='avg':
        metricaTime = df_aux.loc[  df_aux['Festival']==yn_Festival , 'avg_time' ]
    elif type_metric=='std':
        metricaTime = df_aux.loc[  df_aux['Festival']==yn_Festival , 'std_time' ]
    
    metricaTime = np.round( metricaTime, 2 )
    return metricaTime
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função para plotar tempo médio com barra de erro usando desvPad do tempo por Cidade
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def plotBars_tempoCity( df1, cols = [ 'City', 'Time_taken(min)' ]):
    """ FUNÇÃO plot bar chart com o tempo médio ou o desvio padrão do tempo de entrega
    
        Input:  df1          dataframe
                cols         colunas
        Output: fig com o bar chart
    """
    df_aux = df1.loc[ : , cols].groupby( 'City' ).agg( { 'Time_taken(min)': [ 'mean', 'std' ] } )
    df_aux.columns = [ 'avg_time', 'std_time' ]
    df_aux = df_aux.reset_index()
    
    # Arredondar valores
    df_aux['avg_time'] = df_aux.apply(lambda row: np.round( row['avg_time'] , 2) , axis=1)
    df_aux['std_time'] = df_aux.apply(lambda row: np.round( row['std_time'] , 2) , axis=1)
    
    fig = go.Figure()
    fig.add_trace( go.Bar( name='Control' , x=df_aux['City'], y=df_aux['avg_time'], error_y= dict( type='data', array=df_aux['std_time']) ) )
    fig.update_layout( barmode='group' , paper_bgcolor="#F0F0F0")

    return fig
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função para criar os tempos médios por cidade para cada condição do tempo
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def buildDataframe_temposRoadTraffic( df1, cols):
    """ FUNÇÃO cria um dataframe com média e desvio padrão para ver como tabela
    
        Input:  df1          dataframe
                cols         colunas
        Output: dtaframe df_aux
    """
    df_aux = df1.loc[ : , cols]
    df_aux = df_aux.groupby(['City','Road_traffic_density']).agg( {'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time','std_time']

    # Arredondar valores
    df_aux['avg_time'] = df_aux.apply(lambda row: np.round( row['avg_time'] , 2) , axis=1)
    df_aux['std_time'] = df_aux.apply(lambda row: np.round( row['std_time'] , 2) , axis=1)
    return df_aux
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função pie plot com distancias haversine 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
def piePlot_haversineDist( df1, cols ):
    df_aux = df1.loc[ :, cols ].copy()
    
    # Cria uma nova coluna 'distancia_haversine' com as distâncias calculadas usando a função haversine_distance
    df_aux['distancia_haversine'] = df_aux.apply( lambda row: haversine_distance(row) , axis=1 )   # usa a função criada acima
    
    df_aux = df_aux.loc[ :, ['City','distancia_haversine'] ]
    avg_Dist = df_aux.groupby( 'City' ).mean().reset_index()
    
    # Gráfico de pizza com o graphic_object da lib plotly importada como go
    fig = go.Figure(  data=[  go.Pie( labels=avg_Dist['City'] , values=avg_Dist['distancia_haversine'], pull=[0,0.1,0] )  ]   )
    
    return fig
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Função sunburst chat com tempo médio de entrea por tipo de tráfego
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def sunbplot_tempoTraffic( df1, cols ):
    df_aux = ( df1.loc[ : , cols]
              .groupby( [ 'City','Road_traffic_density' ] )
              .agg( { 'Time_taken(min)': [ 'mean', 'std' ] } )
         )
    df_aux.columns = [ 'avg_time', 'std_time' ]
    df_aux = df_aux.reset_index()
    
    # Arredondar valores
    df_aux['avg_time'] = df_aux.apply(lambda row: np.round( row['avg_time'] , 2) , axis=1)
    df_aux['std_time'] = df_aux.apply(lambda row: np.round( row['std_time'] , 2) , axis=1)
    
    fig = px.sunburst( df_aux, path=[ 'City','Road_traffic_density' ], values='avg_time',
                       color='std_time', #color_continuous_scale='RdBu'
                       color_continuous_scale=["blue","red"], color_continuous_midpoint= np.average( df_aux['std_time']) )
    return fig
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Carregar os dados da tabela
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
data_path = r'\Users\HCInsula\Documents\DataScience_Studies\ComunidadeDS\repos\ftc_analisando_dados_python\CurryCompany_app\train.csv'
df = pd.read_csv( data_path )
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
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aviso do horário de execução do .py
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
print( 'Current time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print( "Possui ", len( df1 ) , "entregas na base" )
print( "Quantidade de entregadores", len( df1['Delivery_person_ID'].unique() )  , '\n' )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Layout de visão no StreamLit para dashboards
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
#
#
# Header 1
st.header( 'Marketplace - Visão Restaurantes' )
#
# # st.dataframe( df )                        #  . . . # Shows the dateframe df
#
# Sidebar 1
image_path = r'\Users\HCInsula\Documents\DataScience_Studies\ComunidadeDS\repos\ftc_analisando_dados_python\CurryCompany_app\logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( 'Fastest delivery in town' )
st.sidebar.markdown( """---""" )
#
#
st.sidebar.markdown( '### Filtros' )
#
date_slider = st.sidebar.slider(
    'Selecione a data limite',
    value =   df1['Order_Date'].min().to_pydatetime() + ( df1['Order_Date'].max().to_pydatetime()-df1['Order_Date'].min().to_pydatetime() ) / 2,  #  Standard date
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
st.sidebar.markdown( """---""" )
st.sidebar.markdown( 'Powered by CDS' )
#
#
# Header 2
# st.header( f"Data selecionada:  {date_slider.date()}",   divider='rainbow' )  #  prints the selected value in the slider as a date (doesn't show the time) and draws a rainbow line underneath the text
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aplicação de filtros
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
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
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
#
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )
#
#
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
# Visão Gerencial
#
with tab1:
    with st.container():
        st.title( "Overall Metrics" )
        #
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        #
        with col1:  # Quantidade de entregadores
            delivery_unique = len( df1['Delivery_person_ID'].unique() )
            col1.metric( 'Entregadores', delivery_unique)                    # mostrar medida
            #
        with col2:  # Distancia media
            cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
            distMedia = distanciaMedia( df1, cols)
            col2.metric( 'Dist media (m)', np.round( distMedia, 2 )  )       # mostrar medida
            #
        with col3:  # Tempo médio de entrega no Festival
            metricaTime = tempoFestival_avg_std( df1, yn_Festival='Yes', type_metric='avg' )
            st.metric( 'Festival (min)', metricaTime )
            #
        with col4:  # DesvPad do tempo de Entrega no Festival
            metricaTime = tempoFestival_avg_std( df1, yn_Festival='Yes', type_metric='std' )
            st.metric( 'DesvPad', metricaTime )
            #
        with col5:  # Tempo médio de entrega no Festival
            metricaTime = tempoFestival_avg_std( df1, yn_Festival='No', type_metric='avg' )
            st.metric( 'S/ Festv (min)', metricaTime)
            #
        with col6:  # DesvPad do tempo de Entrega no Festival
            metricaTime = tempoFestival_avg_std( df1, yn_Festival='No', type_metric='std' )
            st.metric( 'DesvPad', metricaTime)
            #
    with st.container():  # Tempo médio de entrega por cidade
        st.markdown( """---""" )
        st.title( "Tempo médio de entrega por cidade" )
        #
        col1, col2 = st.columns( 2 )
        #
        with col1:
            fig = plotBars_tempoCity( df1, cols = [ 'City', 'Time_taken(min)' ])
            st.plotly_chart( fig , use_container_width=True )
        

        with col2:
            st.markdown( 'Ver média e desvio padrão' )
            df_aux = buildDataframe_temposRoadTraffic( df1, cols = ['Time_taken(min)','City','Road_traffic_density'] )
            st.dataframe( df_aux , use_container_width=True)
            
    with st.container():
        st.markdown( """---""" )
        st.title( "Distribuição do Tempo" )

        col1, col2 = st.columns( 2 )

        with col1:
            cols = ['City','Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
            fig = piePlot_haversineDist( df1, cols )
            st.plotly_chart( fig )
            
        with col2:
            fig = sunbplot_tempoTraffic( df1, cols = [ 'City', 'Time_taken(min)', 'Road_traffic_density' ] )
            st.plotly_chart( fig , use_container_width=True )