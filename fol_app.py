import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from app_func import show_objects_on_map, plot_map_tpu, plot_top_by_col
import pandas as pd
from ast import literal_eval

import io
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
st.set_page_config(layout="wide")
def main():
    main_df, tpu_data = load_data()
    page = st.sidebar.selectbox("Выберите страницу", ["Главная", "Карта ТПУ Москвы", 
                                                  "Карта окрестности ТПУ",
                                                  "Графики"])
    translit = st.sidebar.checkbox('Names transliteration')


    if page == "Главная":
        '''
        # Главная страница    
        ## Описание датасета
        В датастете содержится информация о торговых объектах и ближайших к ним транспортно-пересадочных узлов в г. Москва с указанием эффективной зоны охвата объекта. Кроме того в датасете содержится следующая информация:
    
            * Данные о стоимости коммерческой недвижимости в районе объекта
            * Демографические и географические данные о районе объекта
            * Данные о зоне охвата объекта
            * Данные о пассажиропотоке ближайшей станции метро
        Часть данных в датасете представлена в виде словарей, что связано с вложенностью отдельных признаков. К примеру, ряд ТПУ представляют собой комплекс из отдельных объектов наземного и подземного транспорта.
        '''
        info_expander = st.beta_expander('Информация о датасете')
        with info_expander:
            
            buffer = io.StringIO()
            main_df.info(buf=buffer)
            contents = buffer.getvalue().split('\n')
            for lines in contents:
                st.write("<pre>" + lines + "</pre>\n", unsafe_allow_html=True)
        
        st.image("https://i.ibb.co/D4sJgYk/image-1.png", clamp = True)

        st.header("Пример датасета")
        '''
        Здесь вы можете увидеть первые 100 записей.
        '''
        st.write(main_df.head(100), )
        st.header("Список источников")
        '''

        В датасете были использованы следующие данные с сайта [Портал открытых данных](https://data.mos.ru) города Москва:

        [Транспортно-пересадочные узлы](https://data.mos.ru/opendata/7704786030-transportno-peresadochnye-uzly?pageNumber=1&versionNumber=4&releaseNumber=27)
            
        [Стационарные торговые объекты](https://data.mos.ru/opendata/7710881420-statsionarnye-torgovye-obekty?pageNumber=1&versionNumber=1&releaseNumber=22)
            
        [Бытовые услуги на территории Москвы](https://data.mos.ru/opendata/7710881420-bytovye-uslugi-na-territorii-moskvy/data/table?versionNumber=2&releaseNumber=30)

        #### Другие источники:

        Расчет торговой зоны и зоны охвата магазина был произведен на основе статьи ["Расчет торговой зоны и зоны охвата магазина"](http://www.arhitrade.com/education.php?Id=43)
            
        Информация о районах: [Wikipedia: Список районов и поселений Москвы](https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%BE%D0%B2_%D0%B8_%D0%BF%D0%BE%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B)
            
        Информация о ценах на коммерческую недвижимость: [Restate](https://msk.restate.ru/graph/ceny-arendy-kommercheskoy/)
            
        Сведения о пассажиропотоке на станциях: [Рекламное агентство Метро Москвы](https://www.metro-msk.ru/stat/2019/)
            
        [Геоданные](http://gis-lab.info/data/mos-adm/mo.geojson) о форме административных районов и округов Москвы
        '''
    elif page == "Карта ТПУ Москвы":

        st.title("Карта Москвы")
        st.write("Всего ТПУ на карте: ", tpu_data.shape[0])
        st.write("Всего торговых точек: ", main_df.shape[0])
        my_expander = st.beta_expander("Настройки", expanded=True)
        with my_expander:
            c1, c2, c3 = st.beta_columns((0.5, 0.1, 1))
            obj_size = c1.number_input("Сколько объектов отобразить:",
                                   min_value=1, max_value=len(main_df),
                                   value = 1000,step=100)
            obj_as_marker = c3.checkbox("Объекты как маркер")
            display_districts = c3.checkbox("Отобразить районы", value=True)
            display_tpu = c3.checkbox("Отобразить ТПУ", value=True)
            '''
            ** Внимание! Отображение более 10 000 объектов займет много времени! **
            '''
            
        
        
        m = show_objects_on_map(main_df, tpu_data,
                        marker_size=2,
                        zoom=10,
                        obj_as_marker=obj_as_marker,
                        obj_size=obj_size,
                        display_districts=display_districts,
                        display_tpu=display_tpu, 
                        translit=translit)
        folium_static(m, width=1000, height=700)
        
    elif page == "Карта окрестности ТПУ":
        st.title("Карта ТПУ")
        c1, _ = st.beta_columns((2, 1))
        tpu_name = c1.selectbox('Выберите ТПУ:',main_df['tpu_name'].unique())
        m = plot_map_tpu(tpu_name, tpu_data, main_df, translit=translit)
        folium_static(m, width=1000, height=700)

    elif page == "Графики":
        
        st.title("Графики")
        columns_list = ['is_network_object', 'is_tpu_in_coverage',
                        'object_address','object_area', 'object_district',
                        'object_operating_company',
                        'object_service_type', 'object_size',
                        'object_type', 'subway_line',
                        'subway_station', 'tpu_comissioning_year',
                        'tpu_name', 'tpu_near_station', 'tpu_status']
        
        numeric_col = ['is_network_object', 'is_tpu_in_coverage',
                       'object_size', 'tpu_comissioning_year']
        
        col = st.selectbox('Выберите колонку:', columns_list)
        num_top = st.number_input('Отобразить максимум ', min_value=2,
                                  max_value=20,
                                  value = 5)
        if col in numeric_col:
             horizontally=False
        else:
            horizontally=True
            
        p = plot_top_by_col(col, main_df, num_top, '', other=False, translit=translit, 
                    max_string_len=15, horizontally=horizontally, labels =[],
                    palette = sns.color_palette("tab10"))
        st.pyplot(p, clear_figure=p)
        


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