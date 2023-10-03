import folium
import streamlit as st
import branca
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
import plotly.express as px
from folium.features import GeoJsonPopup, GeoJsonTooltip



#location=(30, 10), zoom_start=1.2
df_geo = gpd.read_file("data/edited_geo_df.shp")
#print(list(set(df['continent'])))
#filtered_geo = df.dropna(subset = ['amount_usd'])
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

selected_metric_m = st.selectbox(label = 'Select Geographic Metric',options = ['Count','Amount in Millions'])
selected_continent =  st.selectbox('Select Continent to Analyze', options = continent_list)

selected_metrics = metric_dict[selected_metric_m]

def create_map(df,selected_continent, cont_dict, metric, metric_name):

    m = folium.Map()
    if selected_continent == 'World':
        fcdf = df
    else:
        fcdf = df[df['continent'] == selected_continent]

    colormap = branca.colormap.LinearColormap(
        vmin=fcdf[metric].quantile(0.0),
        vmax=fcdf[metric].quantile(1),
        colors=["red", "blue"],
        caption=metric_name,
    )
    popup = GeoJsonPopup(
        fields=["name", "amount_usd"],
        aliases=["Country: ", metric_name],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = GeoJsonTooltip(
        fields=["name",metric],
        aliases=["Country:", metric_name],
        localize=True,
        sticky=False,
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
    return m, fcdf

# call to render Folium map in Streamlit
outputs = create_map(df_geo, selected_continent, cont_dict,selected_metrics ,selected_metric_m)
m= outputs[0]

st_folium(m, height = 400, width=700)
df_bar = outputs[1][['name',selected_metrics]].dropna().sort_values(selected_metrics,ascending = False)
fig = px.bar(df_bar, x = 'name', y = selected_metrics,height=400, width = 700)
fig.update_layout(title='Amount per Country', yaxis_title= selected_metric_m, xaxis_title='country')
st.plotly_chart(fig)




#st_data2 = st_folium(m, height = 400, width=600, key = 'm')
