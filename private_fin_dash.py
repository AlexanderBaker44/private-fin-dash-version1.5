import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
from folium_mapping_sample import df_geo, create_map, cont_dict, continent_list
import folium
import streamlit as st
import branca
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
import plotly.express as px
from folium.features import GeoJsonPopup, GeoJsonTooltip

st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv('data/preprocessed_funding.csv')

ddf = df
ddf['Month'] = pd.to_datetime(ddf['Month'])

#df_geo = gpd.read_file("data/edited_geo_df.shp")
#print(df_geo)

filtered_geo = df_geo.dropna(subset = ['amount_usd'])
company_list = list(set(df['Company']))
#continent_list = list(set(filtered_geo['continent']))



metric_dict = {'Count':'count', 'Amount in Millions':'amount_usd'}

#tabs general, geographic, single companies
tab1,tab2,tab3 = st.tabs(['General','Company Overview','Geographic'])

#general metrics count and total
with tab1:
    st.header('General Financial Analysis')
    selected_metric_m = st.selectbox(label = 'Select Metric',options = ['Count','Amount in Millions'])
    selected_metric = metric_dict[selected_metric_m]


    if selected_metric_m == 'Count':
        time_investor = ddf.dropna().groupby('Month').count()['Unnamed: 0']

        by_type = df.groupby('Major Category').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector = df.groupby('Subcategory').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']


        by_type_s = df.dropna().groupby('Strategics').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector_s = df.dropna().groupby('Stage').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        selected_metric_s = 'Unnamed: 0'


    elif selected_metric_m == 'Amount in Millions':
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

with tab2:
    st.header('Company Overview')
    selected_companies = st.multiselect('Select Companies to Analyze', company_list,[company_list[0]])
    filtered_df = df[df['Company'].isin(selected_companies)]
    if filtered_df.empty == False:
        st.subheader('Company Investors')
        lgdf = filtered_df.groupby('Company').agg({'Lead Investor': lambda x: list(x)[0],'Other Investor': lambda x: list(set(x))[0]})
        st.table(lgdf)

        st.subheader('Investment Amount in Millions')
        fgdf = filtered_df[['Company','amount_usd','Country']].groupby(['Company']).sum()
        if sum(fgdf['amount_usd']) > 0:
            #fgdf['amount_usd'].plot(kind = 'bar', ylabel = 'Amount in Millions')
            #st.pyplot()
            fig = px.bar(fgdf, x = fgdf.index, y = 'amount_usd',height=400, width = 800)
            fig.update_layout(title='Amount per Companny', yaxis_title='Amount USD', xaxis_title='category')
            st.plotly_chart(fig)
        else:
            st.write('There is no investment amount found for the selected company')
    else:
        st.write('Please Select a Company')

with tab3:
    st.header('Geography Dashboard')
    selected_metric_m = st.selectbox(label = 'Select Geographic Metric',options = ['Count','Amount in Millions'])
    selected_metrics = metric_dict[selected_metric_m]
    selected_continent =  st.selectbox('Select Geographic Body to Analyze', options = continent_list)
    st.subheader('Map')
    outputs = create_map(df_geo, selected_continent, cont_dict,selected_metrics ,selected_metric_m)
    m = outputs[0]

    st_data = st_folium(m, height = 400, width=700)
    st_data
    df_bar = outputs[1][['name',selected_metrics]].dropna().sort_values(selected_metrics,ascending = False)

    st.subheader('Numerical Comparison')
    fig = px.bar(df_bar, x = 'name', y = selected_metrics,height=400, width = 700)
    fig.update_layout(title='Amount per Country', yaxis_title= selected_metric_m, xaxis_title='country')
    st.plotly_chart(fig)



#single company all info written
#selected_companies = st.multiselect()


# Using object notation
