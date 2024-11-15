## Info

In this task, we will create a data pipeline to ingest data from different sources and store them in a database.


````mermaid
graph TD
    %% Data Sources
    A1[GeoData Bavaria](https://geodaten.bayern.de/opengeodata/) --> B[Data Preprocessing]
    A2[3D Building Models NRW](https://www.bezreg-koeln.nrw.de/geobasis-nrw/produkte-und-dienste/3d-gebaeudemodelle) --> B[Data Preprocessing]
    A3[LOD2 Building Data Berlin](https://daten.berlin.de/datensaetze/lod2-geb-udedaten-berlin) --> B[Data Preprocessing]
    
    %% Data Preprocessing Step
    B[Data Preprocessing] --> C[Database Storage]
    
    %% Database to Use Cases
    C[Database Storage] --> D1[GIS Applications Queries geospatial data]
    C[Database Storage] --> D2[Urban Planning Tools Analyzes building data]
    C[Database Storage] --> D3[Public Data Portal Provides accessible datasets]
    C[Database Storage] --> D4[Research Platform Supports academic analysis]
````


Potential data sources are available form the [CityGMLWiki](https://www.citygmlwiki.org/index.php?title=Open_Data_Initiatives_in_Germany).

# Open Data in Germany

| Dataset            | Country | Level of Detail | CRS                                          | CityGML Version | Year                   | Acquisition Technique        | Thematic Classes | Textures | Notes                    |
|--------------------|---------|-----------------|----------------------------------------------|-----------------|------------------------|-----------------------------|------------------|----------|--------------------------|
| Baden-Württemberg  | Germany | LoD2            | ETRS89/UTM                                   | 1.0             | 2023                   | Cadastre footprints + LiDAR | Building         | No       |                          |
| Bayern            | Germany | LoD2            | urn:adv:crs:ETRS89_UTM32*DE_DHHN2016_NH      | 1.0             | 2022                   | Cadastre footprints + LiDAR | Building         | No       |                          |
| Berlin            | Germany | LoD2            | EPSG:4979                                    | 2.0             | 2013                   | ?                           | Building         | Yes      | Released in 2015         |
| Berlin            | Germany | LoD2            | urn:adv:crs:ETRS89_UTM33*DE_DHHN2016_NH      | 1.0             | 2019                   | ?                           | Building         | No       |                          |
| Brandenburg       | Germany | LoD1 / LoD2     | urn:adv:crs:ETRS89_UTM33*DE_DHHN2016_NH      | 1.0             | 2020                   | ?                           | Building         | No       | Released in 2015         |
| Hamburg           | Germany | LoD1 / LoD2     | urn:adv:crs:ETRS89_UTM32*DE_DHHN92_NH        | 1.0             | 2015                   | Cadastre footprints + LiDAR | Building         |          |                          |
| Hessen            | Germany | LoD2            | ETRS89_UTM32*DE_DHHN2016_NH                  | 1.0             | 2021-09-24             |                             | Building         | No       |                          |
| Niedersachsen     | Germany | LoD1 / LoD2     | urn:ogc:def:crs,crs:EPSG:6.12:25832,crs:EPSG:6.12:5783 | 1.0  | 2015           | Cadastre footprints + LiDAR | Building         | No       |                          |
| Nordrhein-Westfalen | Germany | LoD1 / LoD2 | urn:adv:crs:ETRS89_UTM32*DE_DHHN92_NH        | 2.0             | 2017                   | Cadastre footprints + LiDAR | Building         | No       |                          |
| Rheinland-Pfalz   | Germany | LoD2            | urn:ogc:def:crs,crs:EPSG:6.12:25833,crs:EPSG:6.12:5783 | 1.0 | 2020 (Updated 26.02.2020) | | Building | No       |                          |
| Sachsen           | Germany | LoD1 / LoD2     | urn:ogc:def:crs,crs:EPSG:6.12:25833,crs:EPSG:6.12:5783 | 1.0 | 2020 (Updated 26.02.2020) | | Building | No       |                          |
| Sachsen-Anhalt    | Germany | LoD1 / LoD2     | urn:adv:crs:ETRS89_UTM32*DE_DHHN2016_NH      | 1.0             | 2019                   |                             | Building         | No       |                          |
| Thüringen         | Germany | LoD1 / LoD2     | urn:adv:crs:ETRS89_UTM32*DE_DHHN2016_NH      | 1.0             | 2015                   |                             | Building         | No       |                          |


# Related Tools and Projects

- [3D City Database](https://www.3dcitydb.org/)
- [CityDoctor](https://www.hft-stuttgart.de/forschung/projekte/aktuell/citydoctor-2)
