import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
#from folium_mapping_sample import df_geo, create_map, cont_dict, continent_list
import folium
import branca
from streamlit_folium import st_folium
from folium.features import GeoJsonPopup, GeoJsonTooltip

#renderng glitch has to do with tabs
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv('data/preprocessed_funding.csv')

ddf = df
ddf['Month'] = pd.to_datetime(ddf['Month'])

#df_geo = gpd.read_file("data/edited_geo_df.shp")
#print(df_geo)
df_geo = gpd.read_file("data/edited_geo_df.shp")
filtered_geo = df_geo.dropna(subset = ['amount_usd'])
company_list = list(set(df['Company']))
#continent_list = list(set(filtered_geo['continent']))


metric_dict = {'Count':'count', 'Amount in Millions':'amount_usd'}
cont_dict = {
'World': [[-50.003431,-175.781123],[78.091047,188.676738]],
'North America': [[-2.600651,-130.909825],[69.778954,-63.856951]],
#'South America': [[-58.704332,-89.218864],[9.726405,-28.006829]],
'Africa': [[-37.020096,-15.406895],[36.738886,40.176447]],
'Europe': [[33.049188,-21.598470],[70.104502,49.111984]],
'Asia': [[7.536767,32.480595],[54.876608,150.260988]],
'Oceania': [[-41.692597,96.366250],[6.070650,187.128922]]
}


continent_list = list(cont_dict.keys())


metric_dict = {'Number of Investments':'count', 'Amount in Millions USD':'amount_usd'}

with st.sidebar:
    page  = st.radio('Choose Page', ('General', 'Company Overview', 'Geographic'))
#tabs general, geographic, single companies
#tab1,tab2,tab3 = st.tabs(['General','Company Overview','Geographic'])

#general metrics count and total
if page == 'General':
    st.header('General Financial Analysis')
    selected_metric_m = st.selectbox(label = 'Select Metric',options = ['Number of Investments','Amount in Millions USD'])
    selected_metric = metric_dict[selected_metric_m]


    if selected_metric_m == 'Number of Investments':
        time_investor = ddf.dropna().groupby('Month').count()['Unnamed: 0']

        by_type = df.groupby('Major Category').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector = df.groupby('Subcategory').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']


        by_type_s = df.dropna().groupby('Strategics').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector_s = df.dropna().groupby('Stage').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        selected_metric_s = 'Unnamed: 0'


    elif selected_metric_m == 'Amount in Millions USD':
        #print(selected_metric_m)
        time_investor = ddf.dropna().groupby('Month').sum()['amount_usd']
        print(time_investor)
        by_type = df[['Major Category','amount_usd']].groupby('Major Category').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        by_sector = df[['Subcategory','amount_usd']].groupby('Subcategory').sum().sort_values('amount_usd',ascending=False)['amount_usd']


        by_type_s = df[['Strategics','amount_usd']].dropna().groupby('Strategics').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        by_sector_s = df[['Stage','amount_usd']].dropna().groupby('Stage').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        selected_metric_s = metric_dict[selected_metric_m]


    st.subheader('Monthly Analysis')
    #figt, mnxt = plt.subplots(1, 1)
    #time_investor.plot(kind = 'line', figsize = (20,10), title = 'Investments Made Over Time', ylabel = f'{selected_metric_m}')
    #st.pyplot()
    fig = px.line(time_investor, x = time_investor.index, y = selected_metric_s,height=400, width = 800)
    fig.update_layout(title='Time Analysis', yaxis_title=selected_metric_m, xaxis_title='month')
    st.plotly_chart(fig)


    st.subheader('Investor Categories')
    col1,col2 = st.columns(2)
    with col1:
        #figmx, mnx = plt.subplots(1, 1)
        #by_type.plot(ax = mnx, kind = 'bar',title = 'Investments by Category', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_type, x = by_type.index, y = selected_metric_s,height=400, width = 400)
        fig.update_layout(title='Category', yaxis_title=selected_metric_m, xaxis_title='category')
        st.plotly_chart(fig)

    with col2:
        #figmxv, mnxv = plt.subplots(1, 1)
        #by_sector.plot(ax = mnxv, kind = 'bar',title = 'Investments by Subcategory', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_sector, x = by_sector.index, y = selected_metric_s, height=400, width = 400)
        fig.update_layout(title='Subcategory', yaxis_title=selected_metric_m, xaxis_title='subcategory')
        st.plotly_chart(fig)

    st.subheader('Additional Investment Information')
    col1,col2 = st.columns(2)
    with col1:
        #by_sector_s.plot(kind = 'bar',title = 'Investments by Stage', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_sector_s, x = by_sector_s.index, y = selected_metric_s, height=400, width = 400)
        fig.update_layout(title='Stage', yaxis_title=selected_metric_m, xaxis_title='stage')
        st.plotly_chart(fig)
    with col2:
        #by_type_s.plot(kind = 'bar',title = 'If Investment is Strategic', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_type_s, x = by_type_s.index, y = selected_metric_s, height=400, width = 400)
        fig.update_layout(title='Strategics', yaxis_title=selected_metric_m, xaxis_title='strategics')
        st.plotly_chart(fig)




#geographic, count and total toggle

#selected_metric = st.dropdown()

if page == 'Company Overview':
    st.header('Company Overview')
    selected_companies = st.multiselect('Select Companies to Analyze', company_list,[company_list[0]])
    filtered_df = df[df['Company'].isin(selected_companies)]
    if filtered_df.empty == False:
        st.subheader('Company Investors')
        lgdf = filtered_df.groupby('Company').agg({'Lead Investor': lambda x: list(x)[0],'Other Investor': lambda x: list(set(x))[0]})
        st.table(lgdf)

        st.subheader('Investment Amount in Millions USD')
        fgdf = filtered_df[['Company','amount_usd','Country']].groupby(['Company']).sum()
        if len(fgdf['amount_usd']) > 1:
            #fgdf['amount_usd'].plot(kind = 'bar', ylabel = 'Amount in Millions')
            #st.pyplot()
            fig = px.bar(fgdf, x = fgdf.index, y = 'amount_usd',height=400, width = 800)
            fig.update_layout(title='Amount of Investments per Company', yaxis_title='Amount in Millions USD', xaxis_title='category')
            st.plotly_chart(fig)
        elif len(fgdf['amount_usd']) == 1:
            comp_val = list(fgdf['amount_usd'])[0]
            st.markdown(f'#### The company {list(fgdf.index)[0]} has {comp_val} million USD.')
        else:
            st.write('There is no investment amount found for the selected company')
    else:
        st.write('Please Select a Company')

if page  == 'Geographic':


    st.header('Geography Dashboard')
    metric_name = st.selectbox(label = 'Select Geographic Metric',options = ['Number of Investments','Amount in Millions USD'], index = 1)
    metric = metric_dict[metric_name]
    selected_continent =  st.selectbox('Select Geographic Body to Analyze', options = continent_list)
    m = folium.Map()
    st.subheader('Map')
    #print(selected_continent)
    m.fit_bounds(cont_dict[selected_continent])

    if selected_continent == 'World':
        fcdf = df_geo
    else:
        fcdf = df_geo[df_geo['continent'] == selected_continent]

    colormap = branca.colormap.LinearColormap(
        vmin=fcdf[metric].quantile(0.0),
        vmax=fcdf[metric].quantile(1),
        colors=["red", "blue"],
        caption=metric_name,
    )
    popup = GeoJsonPopup(
        fields=["name", metric],
        aliases=["Country: ", f'{metric_name}: '],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = GeoJsonTooltip(
        fields=["name", metric],
        aliases=["Country: ", f'{metric_name}: '],
        localize=True,
        sticky=True,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )


    folium.GeoJson(
        fcdf,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"][metric])
            if x["properties"][metric] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
        popup=popup,
    ).add_to(m)

    colormap.add_to(m)


    m.fit_bounds(cont_dict[selected_continent])



    st_data = st_folium(m, height = 400, width=700)
    df_bar = fcdf[['name',metric]].dropna().sort_values(metric ,ascending = False)

    st.subheader('Numerical Comparison')
    if len(df_bar['name']) > 1:
        fig = px.bar(df_bar, x = 'name', y = metric,height=400, width = 700)
        fig.update_layout(title='Amount per Country', yaxis_title= metric_name, xaxis_title='country')
        st.plotly_chart(fig)
    elif len(df_bar['name']) == 1:
        cont_val = list(df_bar[metric])[0]
        name_cont = list(df_bar['name'])[0]
        st.markdown(f'#### The company {name_cont} has {cont_val} million USD.')
    else:
        st.write('Continent has no relevant investments.')



#single company all info written
#selected_companies = st.multiselect()


# Using object notation
