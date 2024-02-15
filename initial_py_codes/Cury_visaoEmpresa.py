# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Importar libraries
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from haversine import haversine  # para calcular a distância entre dois pontos geográficos

import os
os.add_dll_directory('C:\\Users\\HCInsula\\Miniconda\\DLLs')  # para dar certo as dependências

import streamlit as st   # to display things in Streamlit API
# To install streamlit use  conda install conda-forge::streamlit  in Anaconda Prompt

from datetime import datetime  # to work with dates and times

from PIL import Image    # to bring images to show in StreamLit
# pip install folium
# pip install streamlit-folium

import folium                               # to things on maps
from streamlit_folium import folium_static  # to indeed show the map
    

# to install folium and streamlit-folium go to Miniconda prompt and run the following lines
# conda activate py311                                # this activates the virtual environment py312, in which has Python 3.12
# conda install conda-forge::streamlit-folium        # 

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Carregar os dados da tabela
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
df = pd.read_csv('train.csv')


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Limpeza de dados
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
df1 = df.copy()

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


# Converter de object para tipos apropriados
df1 = df1.astype({'Delivery_person_Age':'int64',
                  'Delivery_person_Ratings':'float64',
                  'multiple_deliveries':'int64',
                  'Vehicle_condition':'int64'})

# converter a "Order Date" para datetime
df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y')
# df1['Time_Orderd'] = pd.to_datetime( df1['Time_Orderd'], format='%H:%M:%S')
# df1['Time_Order_picked'] = pd.to_datetime( df1['Time_Order_picked'], format='%H:%M:%S')


# Tirar espaços que sobram
df1.loc[:, ['ID']]                   = df1.loc[:, ['ID']                   ].squeeze().str.strip()
df1.loc[:, ['Delivery_person_ID']]   = df1.loc[:, ['Delivery_person_ID']   ].squeeze().str.strip()
df1.loc[:, ['Road_traffic_density']] = df1.loc[:, ['Road_traffic_density'] ].squeeze().str.strip()
df1.loc[:, ['Type_of_order']]        = df1.loc[:, ['Type_of_order']        ].squeeze().str.strip()
df1.loc[:, ['Type_of_vehicle']]      = df1.loc[:, ['Type_of_vehicle']      ].squeeze().str.strip()
df1.loc[:, ['City']]                 = df1.loc[:, ['City']                 ].squeeze().str.strip()
df1.loc[:, ['Festival']]             = df1.loc[:, ['Festival']                 ].squeeze().str.strip()

# Throw away the substring 'conditions ' from field ['Weatherconditions']
# and '(min) ' from field ['Time_taken(min)']
df1 = df1.replace({'Weatherconditions': 'conditions ','Time_taken(min)': r"\(.*\) "},                   {'Weatherconditions': '','Time_taken(min)': ""}, regex=True)
# or  df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )

df1 = df1.astype({'Time_taken(min)':'int64'})

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aviso do horário de execução do .py
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
print( 'Current time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print( "Possui ", len( df1 ) , "entregas na base\n" )


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Layout de visão no StreamLit para dashboards
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

# Header 1
st.header( 'Marketplace - Visão Cliente' )

# # st.dataframe( df )                        #  . . . # Shows the dateframe df

# Sidebar 1
image_path = 'logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( 'Fastest delivery in town' )
st.sidebar.markdown( """---""" )


st.sidebar.markdown( '### Filtros' )

date_slider = st.sidebar.slider(
    'Selecione a data limite',
    value=    df1['Order_Date'].min().to_pydatetime() + (df1['Order_Date'].max().to_pydatetime()-df1['Order_Date'].min().to_pydatetime()) / 2,  #  Standard date
    # value=    df1['Order_Date'].max().to_pydatetime() - datetime.timedelta(days=10),    # alternative to Standard date
    min_value=df1['Order_Date'].min().to_pydatetime() ,
    max_value=df1['Order_Date'].max().to_pydatetime() ,
    format='DD-MM-YYYY'
)

st.sidebar.markdown( """---""" )
trafficOptions = st.sidebar.multiselect(
    'Selecione as condições de trânsito',
    ['Low','Medium','High','Jam'],
    ['Low','High'])


st.sidebar.markdown( """---""" )
st.sidebar.markdown( 'Powered by CDS' )


# Header 2
# st.header( f"Data selecionada:  {date_slider.date()}",   divider='rainbow' )  #  prints the selected value in the slider as a date (doesn't show the time) and draws a rainbow line underneath the text


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aplicação de filtros
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[ linhas_selecionadas, :]

# Filtro de condição de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( trafficOptions )
df1 = df1.loc[ linhas_selecionadas, :]


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Visualizações das análises
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
#
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
# Visão Gerencial
with tab1:
    
    ### 1. Quantidade de pedidos por dia.
    # > **Saída**: Um gráfico de barra com a quantidade de entregas no eixo Y e os dias no eixo X.
    # > **Processo**: Fazer um contagem da colunas “ID” agrupado “Order Date” e usar
    # uma bibliotecas de visualização para mostrar o gráfico de barras.
    # > **Entrada**: Eu posso usar o comando `.groupby()` para agrupar os dados e o
    # comando `.count()` para contar a coluna de IDs e um comando para desenhar um gráfico de barras.
    
    # Selecionar colunas
    cols = ['ID','Order_Date']
    
    # # Definir linhas
    df_aux = df1.loc[ : , cols].groupby( ['Order_Date'] ).count().reset_index()

    # Containers para organizar a página
    with st.container():
        st.markdown( '## Pedidos por dia' )
    
        # # Desenhar gráfico de barras com a Plotly library
        fig = px.bar( df_aux, x='Order_Date', y='ID')
        st.plotly_chart( fig, use_container_width=True )

    with st.container(): # Novo container
        col1, col2 = st.columns( 2 )   # quebrado em 2 colunas
        with col1:
            st.markdown( '### Entregadores por cidade' )

            cols = ['Delivery_person_Age','City']
            dfaux = df1.loc[ : , cols ].groupby( 'City' ).mean().reset_index()
            
            fig = px.pie( dfaux, values='Delivery_person_Age', names='City')
            st.plotly_chart( fig, use_container_width=True)
            
        with col2:
            st.markdown( '### Entregadores por cidade e tráfego' )

            df_aux = df1.loc[ ( df1['Road_traffic_density'] != 'NaN') & ( df1['City'] != 'NaN') , ['ID','Road_traffic_density','City']]
            df_aux = df_aux.groupby( ['Road_traffic_density','City'] ).count().reset_index()
            
            fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
            st.plotly_chart( fig, use_container_width=True )
            
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
# Visão Tática
with tab2:
    st.markdown( '# Por semana' )

    with st.container():
        ### 2. Quantidade de pedidos por semana.
        #> **Saída**: Um gráfico de linhas com a quantidade de entregas no eixo Y e as semanas no eixo X
        #> **Processo**: Eu preciso criar uma coluna a partir da extração dos números da semana da coluna “Order Date”, fazer um contagem da colunas “ID”
        # agrupado pela nova coluna e usar uma bibliotecas de visualização para mostrar o gráfico de linhas.
        #> **Entrada**: Eu posso usar o comando `.groupby()` para agrupar os dados e o
        # comando `.count()` para contar a coluna de IDs e um comando para desenhar um gráficos de linhas.
        # Primeiro encontrar as semanas do ano
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U') # Colocando %W usa a segunda-feira como o primeiro dia da semana; %U é domingo
        df_aux = df1.loc[:, ['ID','week_of_year']].groupby( ['week_of_year'] ).count().reset_index()
        
        fig = px.line( df_aux, x='week_of_year', y='ID')
        st.plotly_chart( fig, use_container_width=True )

    with st.container():
        ### 3. Desenhe um gráfico de barras, mostrando as avaliações médias das entregas por semana.

        # **Saída**: Gráfico de barras com as avaliações no y e as semanas no x.
        
        # **Processo**: Encontrar as semanas baseando-se nas 'Order_Date'. Agrupar as avaliações com a média e usando como grupos as semanas. Plotar o gráfico de barras usando as médias das avaliações no y e as semanas no x.
        
        # **Entrada**: Selecionar as colunas `'Delivery_person_Ratings'` e `'Order_Date'`. Criar a coluna para semanas do ano chamada 'Week', usando  o campo `'Order_Date'` com o comando `.dt.strftime('%U')` sobre o `df1`. Depois, agrupar as semanas com `.groupby('Week').mean()`. Por fim, plotar o gráfico de barras com `px.bar()`.
        
        cols = ['Delivery_person_Ratings','Order_Date']
        dfaux = df1.loc[:,cols]
        dfaux['Week'] = df1['Order_Date'].dt.strftime('%U')        
        dfaux = dfaux[['Delivery_person_Ratings','Week']].groupby('Week').mean().reset_index()
        
        fig = px.bar(dfaux, x='Week',y='Delivery_person_Ratings')
        fig.update_xaxes(type='category')
        fig.update_yaxes(
            range=(4.6, 4.66),
            constrain='domain'
        )
        st.plotly_chart( fig, use_container_width=True )


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
# Visão Geográfica
with tab3:
    st.markdown( '# Mapas' )
    
    # Selecionar colunas
    cols1 = [
            'City','Road_traffic_density',    # 'City' é a região da cidade
            'Restaurant_latitude', 'Restaurant_longitude'
            ]
    cols2 = [
            'City','Road_traffic_density',    # 'City' é a região da cidade
            'Delivery_location_latitude', 'Delivery_location_longitude'
            ]
    
    df_aux1 = df1.loc[ :, cols1]
    df_aux2 = df1.loc[ :, cols2]
    
    # Restaurants
    # mediana das latitudes e das longitudes
    df_aux1 = df_aux1.groupby( ['City','Road_traffic_density'] ).median().reset_index()
    
    # Deliveries
    # mediana das latitudes e das longitudes
    df_aux2 = df_aux2.groupby( ['City','Road_traffic_density'] ).median().reset_index()
    
    
    # # PLOTAR O MAPA
    map = folium.Map()

    for index, location_info in df_aux2.iterrows():
      folium.Marker( [ location_info['Delivery_location_latitude'] , location_info['Delivery_location_longitude'] ],
                     popup=location_info[['City','Road_traffic_density']]
                    ).add_to( map )
    
    folium_static( map, width=1024, height=600 )