import os
import math
import numpy as np
import pandas as pd
import geopandas as gpd
from lxml import etree
from shapely.geometry import Polygon
from pyproj import CRS

def parse_gml(gml_file):
    ns = {
        'gml': 'http://www.opengis.net/gml',
        'bldg': 'http://www.opengis.net/citygml/building/1.0',
        'core': 'http://www.opengis.net/citygml/1.0',
        'gen': 'http://www.opengis.net/citygml/generics/1.0'
    }

    tree = etree.parse(gml_file)
    root = tree.getroot()

    # Manuelle Setzung des CRS auf EPSG:25833 (ETRS89 / UTM Zone 33N)
    crs = CRS.from_epsg(25833)

    # Liste zur Speicherung der Ergebnisse
    roofs_data = []

    # Alle Dachflächen (RoofSurface) extrahieren
    roof_surfaces = root.xpath('//bldg:RoofSurface', namespaces=ns)

    for roof in roof_surfaces:
        # Polygonkoordinaten extrahieren
        pos_list_elements = roof.xpath('.//gml:posList', namespaces=ns)
        if not pos_list_elements:
            continue  # Keine Geometriedaten vorhanden

        for pos_list in pos_list_elements:
            coords_text = pos_list.text.strip()
            coords = list(map(float, coords_text.split()))
            # Koordinaten in Tripel (x, y, z) umwandeln
            coords = [coords[i:i+3] for i in range(0, len(coords), 3)]

            # 3D-Polygon erstellen
            poly_3d = [(x, y, z) for x, y, z in coords]
            # 2D-Polygon für Geometrie (x, y)
            poly_2d = [(x, y) for x, y, z in coords]
            polygon = Polygon(poly_2d)
            if not polygon.is_valid or polygon.is_empty:
                continue  # Ungültiges Polygon

            # Neigungsberechnung
            normal_vector = calculate_normal_vector(coords)
            if normal_vector is None:
                continue
            slope = calculate_slope(normal_vector)
            aspect = calculate_aspect(normal_vector)

            # Fläche berechnen
            area = polygon.area

            # Geometrie in GeoDataFrame speichern
            roofs_data.append({
                'neigung': slope,
                'ausrichtung': aspect,
                'fläche': area,
                'geometry': polygon
            })

    # GeoDataFrame erstellen
    gdf = gpd.GeoDataFrame(roofs_data, crs=crs)
    return gdf

def calculate_normal_vector(coords):
    # Berechnet den Normalenvektor eines Polygons
    if len(coords) < 3:
        return None
    p1 = np.array(coords[0])
    p2 = np.array(coords[1])
    p3 = np.array(coords[2])
    v1 = p2 - p1
    v2 = p3 - p1
    normal = np.cross(v1, v2)
    norm = np.linalg.norm(normal)
    if norm == 0:
        return None
    normal_normalized = normal / norm
    return normal_normalized

def calculate_slope(normal_vector):
    # Neigung aus dem Normalenvektor berechnen
    slope_rad = np.arccos(abs(normal_vector[2]))
    slope_deg = np.degrees(slope_rad)
    return slope_deg

def calculate_aspect(normal_vector):
    # Ausrichtung aus dem Normalenvektor berechnen
    aspect_rad = math.atan2(normal_vector[1], normal_vector[0])
    aspect_deg = (math.degrees(aspect_rad) + 360) % 360
    return aspect_deg

if __name__ == "__main__":
    # Pfad zum Skriptverzeichnis
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Relativer Pfad zur GML-Datei
    gml_relative_path = os.path.join('..', 'data', 'processed', 'Berlin', 'Mierendorffinsel_Berlin.gml')
    gml_file_path = os.path.normpath(os.path.join(script_dir, gml_relative_path))

    # Prüfen, ob die GML-Datei existiert
    if not os.path.exists(gml_file_path):
        print(f"GML-Datei nicht gefunden: {gml_file_path}")
    else:
        gdf = parse_gml(gml_file_path)
        print(gdf.head())  # Ausgabe der ersten Zeilen des GeoDataFrames

        # Optional: GeoDataFrame in Datei speichern (z. B. als GeoJSON)
        output_relative_path = os.path.join('..', 'data', 'processed', 'Berlin', 'dachflaechen.geojson')
        output_path = os.path.normpath(os.path.join(script_dir, output_relative_path))
        gdf.to_file(output_path, driver='GeoJSON')
        print(f"Ergebnisse gespeichert in: {output_path}")
