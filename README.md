# Торговые точки вблизи ТПУ, г.Москва

<img align="right" width="100" height="100" src="https://i.ibb.co/TbyCPm8/logoza-ru-1.png">

## Команда «Data SkyScrapers»

\
ФИЛИППЕНКО Артем, ГАБИТОВ Ильдар, КАНДЫБИН Вячеслав,  КОМПАНИЕЦ Юлия, ПЕТРОВ Егор


## Описание датасета

В датасете содержится информация о торговых точках и их принадлежность к зоне охвата размещенных вблизи транспортно-пересадочных узлов в городе Москва. Кроме того в датасете содержится следующая информация:
* Данные о стоимости коммерческой недвижимости в районе объекта
* Демографические и географические данные о районе объекта
* Данные о зоне охвата объекта

Датасет может быть использован для выбора места расположения новой торговой точки по критерию "наиболее благоприятные условия (низкая плотность конкурентов и высокий уровень пассажиропотока)".

<img align="center" src="https://i.ibb.co/DMjn01Q/image-1.png">

## Источники

В датасете были использованы следующие данные с сайта [Портал открытых данных](https://data.mos.ru):

* [Транспортно-пересадочные узлы](https://data.mos.ru/opendata/7704786030-transportno-peresadochnye-uzly?pageNumber=1&versionNumber=4&releaseNumber=27)
* [Стационарные торговые объекты](https://data.mos.ru/opendata/7710881420-statsionarnye-torgovye-obekty?pageNumber=1&versionNumber=1&releaseNumber=22)
* [Бытовые услуги на территории Москвы](https://data.mos.ru/opendata/7710881420-bytovye-uslugi-na-territorii-moskvy/data/table?versionNumber=2&releaseNumber=30)

Расчет торговой зоны и зоны охвата магазина был произведен на основе статьи ["Расчет торговой зоны и зоны охвата магазина"](http://www.arhitrade.com/education.php?Id=43). <br/> 
Информация о районах: [Wikipedia: Список районов и поселений Москвы](https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%BE%D0%B2_%D0%B8_%D0%BF%D0%BE%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B). <br/> 
Информация о ценах на коммерческую недвижимость: [Restate](https://msk.restate.ru/graph/ceny-arendy-kommercheskoy/). <br/> 

## Методы сбора и обработки

В качестве основы датасета были взяты данные с сайта [Портал открытых данных](https://data.mos.ru), и далее собраны в единый датасет с применением библиотеки **pandas**.
Для сбора данных по зонам охвата магазинов и информации по районам города Москва были использованны методы парсинга с применением библиотек **requests**, **lxml** и **BeautifulSoup**.
Для визуализации объектов на карте была использована библиотека **[Folium](https://python-visualization.github.io/folium/index.html)**.

## Структура репозитория


    .                   
    ├── data                    # датасеты из открытых источников
    │   ├── realty_cost.xlsx            # стоимость аренды и покупки помещения, г.Москва       
    │   ├── tpu.xlsx                    # информация о ТПУ, г.Москва            
    │   ├── Бытовые услуги.xlsx         # информация о торговых точках, г.Москва
    │   └── стационарные объекты.xlsx   # информация о торговых точках, г.Москва              
    ├── middle_results.json     # структура датасета в формате json
    ├──02_team_hak_19_10.ipynb  # ноутбук с кодом
    └── README.md



## Структура датасета

Датасет состоит из 39 столбцов и 78086 строк.


| **Название** | **Описание** | **Тип** | **Значения** |
| ------ | ------ | ------ | ------ |
| **object_global_id** | id торгового объекта (ТО)| int |  |
| **object_name** | Название ТО| str | |
| **is_network_object** | Является ли ТО сетевым | int | 0 = не сетевой объект, <br/> 1 = сетевой объект |
| **is_tpu_in_coverage** | Находится ли ТО в зоне покрытия ТПУ | int | 0 = нет, <br/> 1 = да|
| **object_operating_company** | Управляющая компания ТО | str | |
| **object_service_type** | Тип предоставляемой услуги ТО | str | |
| **object_type** | Тип ТО  | str | |
| **object_area** | Административный округ ТО| str | |
| **object_district** | Район ТО | str| |
| **object_address** | Адрес ТО | str ||
| **object_phone** | Номер телефона ТО | str | |
| **object_working_hours** | Время работы ТО | str | |
| **object_working_hours_clarification** | Уточнение времени работы ТО | str | |
| **object_size** | Размер ТО | int | 1 = маленький, <br/> 2 = средний, <br/>  3 = большой |
| **object_longitude** | Координаты расположения ТО: долгота | float | |
| **object_latitude** | Координаты расположения ТО: широта | float | |
| **object_real_reach_distance** | Зона охвата ТО | float | 2000.0, 4000.0, 10000.0 |
| **distance_to_tpu** | Расстояния от ТО до ближайшего ТПУ, метры | float | |
| **tpu_name** | Название транспортно-пересадочного узла (ТПУ)| str | |
| **tpu_global_id** | id ТПУ | float | |
| **tpu_district** | Район, в котором находится ТПУ | str | |
| **tpu_near_station** | Ближайшая к ТПУ станция| str | |
| **tpu_comissioning_year** | Год сдачи ТПУ в эксплуатацию | float | |
| **tpu_status** | Статус ТПУ | str | проект, построен, строится |
| **tpu_available_transfer**| Доступные виды трансфера ТПУ | str | |
| **tpu_car_capacity** | Количество машино-мест возле ТПУ | float | |
| **tpu_longitude** | Координаты расположения ТПУ: долгота | float | |
| **tpu_latitude** | Координаты расположения ТПУ: широта | float | |
| **object_district_square_m2** | Площадь района, в котором находится ТО, м2 | float | |
| **object_district_population** | Население района, в котором находится ТО | float | |
| **object_district_population_density** | Плотность населения района, в котором находится ТО | float | |
| **object_district_living_space_m2** | Площадь жилого фонда района, в котором находится ТО | float | |
| **object_district_living_space_m2_per_person** | Жилплощадь на человека района, в котором находится ТО | float | |
| **object_district_building_property_price_per_m2** | Цена продажи м2 здания для района, в котором находится ТО | float | |
| **object_district_tradeplace_property_price_per_m2** | Цена продажи м2 торгового помещения для района, в котором находится ТО | float  | |
| **object_district_generalplace_property_price_per_m2** | Цена продажи м2 помещения свободного назначения для района, в котором находится ТО | float | |
| **object_district_building_rent_price_per_m2** | Цена аренды м2 здания для района, в котором находится ТО | float | |
| **object_district_tradeplace_rent_price_per_m2**| Цена аренды м2 торгового помещения для района, в котором находится ТО | float | |
| **object_district_generalplace_rent_price_per_m2**| Цена продажи м2 помещения свободного назначения для района, в котором находится ТО | float | |





