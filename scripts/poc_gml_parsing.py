import pandas as pd
import geopandas as gpd
from lxml import etree
from shapely.geometry import Polygon
import numpy as np
import requests

def calculate_slope_and_aspect(polygon):
    """
    Calculates the slope and aspect of a surface based on its polygon coordinates.

    Args:
        polygon (shapely.geometry.Polygon): The 3D polygon representing the surface.

    Returns:
        tuple: A tuple containing:
            - slope (float): The slope of the surface in degrees (0° = horizontal, 90° = vertical).
            - aspect (float): The aspect of the surface in degrees (0° = north, 90° = east, 180° = south, 270° = west).
            Returns (None, None) if the calculation is not possible.
    """
    coords = np.array(polygon.exterior.coords[:-1])  # Schließe das letzte wiederholte Koordinatenpaar aus
    if coords.shape[0] < 3:
        return None, None  # Kein gültiges 3D-Polygon
    
    # Berechnung der Normalenvektoren aus den ersten drei Punkten
    vec1 = coords[1] - coords[0]
    vec2 = coords[2] - coords[0]
    normal = np.cross(vec1, vec2)
    norm = np.linalg.norm(normal)
    
    if norm == 0:
        return None, None  # Degenerierte Fläche
    
    normal = normal / norm  # Normalisierte Normale
    
    # Neigung (Slope) berechnen (Winkel zwischen Normalvektor und Z-Achse)
    slope = np.arccos(abs(normal[2])) * 180 / np.pi
    
    # Ausrichtung (Aspect) berechnen (Winkel relativ zu Nord im Uhrzeigersinn)
    aspect = (np.arctan2(normal[1], normal[0]) * 180 / np.pi + 360) % 360
    
    return slope, aspect

def process_gml_to_geodataframe(file_path):
    """
    Processes a GML file and extracts information about roof surfaces, including ID, area,
    slope, aspect, and both original geometry and centroid.

    Args:
        file_path (str): The path to the GML file.

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame with the following columns:
            - id (str): The ID of the roof surface.
            - area (float): The area of the roof surface in square meters.
            - slope (float): The slope of the roof surface in degrees.
            - aspect (float): The aspect of the roof surface in degrees.
            - geometry (Polygon): The original geometry of the roof surface.
            - centroid (Point): The centroid of the roof surface.
    """
    # Namespaces for GML and CityGML tags
    ns_building = "http://www.opengis.net/citygml/building/1.0"
    ns_gml = "http://www.opengis.net/gml"

    # Parse the GML file
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Collect data
    roof_data = []

    for roof_surface in root.findall(f".//{{{ns_building}}}RoofSurface"):
        surface_id = roof_surface.attrib.get("{http://www.opengis.net/gml}id", "unknown")
        for polygon in roof_surface.findall(f".//{{{ns_gml}}}Polygon"):
            exterior = polygon.find(f".//{{{ns_gml}}}exterior")
            if exterior is not None:
                pos_list = exterior.find(f".//{{{ns_gml}}}posList")
                if pos_list is not None:
                    coords = list(map(float, pos_list.text.split()))
                    coords = [(coords[i], coords[i + 1], coords[i + 2]) for i in range(0, len(coords), 3)]
                    poly = Polygon(coords)
                    if poly.is_valid:
                        # Calculate slope and aspect
                        slope, aspect = calculate_slope_and_aspect(poly)
                        roof_data.append({
                            "id": surface_id,
                            "area": poly.area,
                            "slope": slope,
                            "aspect": aspect,
                            "geometry": poly,
                            "centroid": poly.centroid,
                        })

    # Convert results to a GeoDataFrame
    gdf = gpd.GeoDataFrame(roof_data, geometry="geometry").set_crs('EPSG:25833').to_crs('EPSG:4326')
    gdf["centroid"] = gdf["geometry"].centroid  # Ensure centroid is added as a separate column

    return gdf



def calculate_pv_potential(data):
    """
    Calculates the photovoltaic (PV) potential for a list of roof surfaces using the PVGIS API.

    Args:
        data (pandas.DataFrame): A DataFrame containing the following columns:
            - centroid_x (float): X-coordinate of the centroid.
            - centroid_y (float): Y-coordinate of the centroid.
            - slope (float): The slope of the roof surface in degrees.
            - aspect (float): The aspect of the roof surface in degrees.

    Returns:
        list: A list of API responses (JSON) for each roof surface. In case of errors, the list contains the corresponding error logs.
    """
    
    eta = 0.2
    for index, row in data.iterrows():
        params = {
            'lat': row['centroid'].y,
            'lon': row['centroid'].x,
            'angle': row['slope'],
            'aspect': row['aspect'] -180,
            'peakpower': row['area']*0.7*eta,  # Standardmäßig 1 kW
            'loss': 14,      # Standardverlustfaktor
            'pvtechchoice': 'crystSi',  # PV-Modultyp: kristallines Silizium
            'mountingplace': 'building',
            'outputformat': 'json'
        }
        response = requests.get('https://re.jrc.ec.europa.eu/api/v5_2/PVcalc', params=params)
        if response.status_code == 200:
            pv_potential = response.json()['outputs']['totals']['fixed']['E_y']
            data.at[index, 'pv_potential'] = pv_potential
    return data


# Beispielverwendung
file_path = "data/processed/Berlin/Mierendorffinsel_Berlin.gml"  # Pfad zur GML-Datei
roof_df = process_gml_to_geodataframe(file_path)
print(roof_df.head())
pv_results = calculate_pv_potential(roof_df.head())
print(pv_results.head())


