import os
import json

import folium
from isochrone_map.constants import (
    MP_DATA_LAT,
    MP_DATA_LONG,
    PATH_BIKING_GEO,
    TOTAL_LAT,
    TOTAL_LONG,
)


# Chemin vers le dossier contenant les fichiers JSON
dossier = "/Users/mazziap/Developer/isochrone_map/isochrone_map/data/geojson_mp_data"

# Liste pour stocker tous les JSON
json_mp_data = []

# Parcours de tous les fichiers du dossier
for nom_fichier in os.listdir(dossier):
    chemin_complet = os.path.join(dossier, nom_fichier)
    timing = chemin_complet[:-8].split("_")[-1]
    with open(chemin_complet, "r", encoding="utf-8") as f:
        data = json.load(f)
        json_mp_data.append((data, timing))

# Affichage ou utilisation
print(f"Nombre de fichiers JSON chargés : {len(json_mp_data)}")

# Chemin vers le dossier contenant les fichiers JSON
dossier = "/Users/mazziap/Developer/isochrone_map/isochrone_map/data/geojson_total"

# Liste pour stocker tous les JSON
json_total = []

# Parcours de tous les fichiers du dossier
for nom_fichier in os.listdir(dossier):
    chemin_complet = os.path.join(dossier, nom_fichier)
    timing = chemin_complet[:-8].split("_")[-1]
    with open(chemin_complet, "r", encoding="utf-8") as f:
        data = json.load(f)
        json_total.append((data, timing))

# Affichage ou utilisation
print(f"Nombre de fichiers JSON chargés : {len(json_total)}")


m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

folium.Marker([MP_DATA_LAT, MP_DATA_LONG], tooltip="MP DATA").add_to(m)
folium.Marker([TOTAL_LAT, TOTAL_LONG], tooltip="Total").add_to(m)


with open(PATH_BIKING_GEO, "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Ordonner du plus long au plus court pour que le court soit au-dessus
feats = sorted(
    geojson["features"], key=lambda f: f["properties"].get("value", 0), reverse=True
)

for idx, feat in enumerate(feats):
    minutes_val = int(round(feat["properties"].get("value", 0) / 60))
    folium.GeoJson(
        data=feat,
        name=f"Biking {minutes_val} min",
        style_function=lambda x: {
            "fillColor": "#137815",
            "color": "#40cc31",
            "weight": 2,
            "fillOpacity": 0.3,
        },
    ).add_to(m)

# # Ajout des polygones isochrones
for geojson, time in json_total:
    folium.GeoJson(
        geojson,
        name=f"Metro Total {time} min",
        style_function=lambda x: {
            "fillColor": "#3186cc",
            "color": "#3186cc",
            "weight": 2,
            "fillOpacity": 0.3,
        },
    ).add_to(m)

# Ajout des polygones isochrones
for geojson, time in json_mp_data:
    folium.GeoJson(
        geojson,
        name=f"Metro MP DATA {time} min",
        style_function=lambda x: {
            "fillColor": "#78134c",
            "color": "#b531cc",
            "weight": 2,
            "fillOpacity": 0.3,
        },
    ).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

m.save("isochrone_transport_paris.html")
