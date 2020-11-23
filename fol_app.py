import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from app_func import show_objects_on_map, plot_map_tpu, plot_top_by_col
import pandas as pd
from ast import literal_eval


import numpy as np
import requests 
import folium
from folium.plugins import FastMarkerCluster
from folium.plugins import BeautifyIcon as BI
from geopy.geocoders import Nominatim 
import json
import branca
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    main_df, tpu_data = load_data()
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Map",
                                                  "Graphics",  "Transport hub map"])

    if page == "Homepage":
        st.header("Homepage")
        st.write("Please select a page on the left.")
        st.write(main_df.head(10))
    elif page == "Map":
        st.title("Transport hubs map")
        m = show_objects_on_map(main_df, tpu_data,
                        marker_size=2,
                        zoom=10,
                        obj_as_marker=False,
                        display_districts=True,
                        display_tpu=True, 
                        translit=False)
        folium_static(m)
    elif page == "Transport hub map":
        tpu_name = st.selectbox('Select transport hub:',main_df['tpu_name'])
        m = plot_map_tpu(tpu_name, tpu_data, main_df)
        folium_static(m)

    elif page == "Graphics":
        col = st.selectbox('Select column:', main_df.columns)
    
        p = plot_top_by_col(col, main_df, 5, '', other=False, translite=False, 
                    max_string_len=15, horizontally=False, labels =[],
                    palette = sns.color_palette("tab10"),
                    figsize=(10, 5))
        st.pyplot(p)
        

@st.cache
def load_data():
    url = 'https://drive.google.com/uc?export=download&id=179ShmAMQsWjTCGHWthf75jCD1lh7WPLC'
    main_df = pd.read_csv(url, sep=';', encoding='cp1251',
                      index_col=0)
    url = 'https://drive.google.com/uc?export=download&id=1cAbeGoe1LMfMCIUqQbkU5qfvh_fJO8O8'
    tpu_data = pd.read_csv(url, sep=';', encoding='cp1251',
                      index_col=0)
    tpu_data.tpu_longitude = tpu_data.tpu_longitude.apply(literal_eval)
    tpu_data.tpu_latitude = tpu_data.tpu_latitude.apply(literal_eval)
    return main_df, tpu_data






if __name__ == "__main__":
    main()