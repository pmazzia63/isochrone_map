import json
import requests
import os
from pprint import pprint
import folium

from isochrone_map.constants import TOTAL_LAT, TOTAL_LONG
from dotenv import load_dotenv


load_dotenv()  # charge le .env

TIMES_RANGES = [300 * i for i in range(1, 11)]
url = (
    "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/isochrones/isochrones"
)
params = {
    "to": f"{TOTAL_LONG};{TOTAL_LAT}",
    "boundary_duration[]": TIMES_RANGES,
    "first_section_mode[]": "walking",
    "forbidden_uris[]": [
        "physical_mode:Tramway",
        "physical_mode:Bus",
        "physical_mode:Bike",
        "physical_mode:BikeSharingService",
    ],
    "datetime": "2025-09-01T08:00:00",
}

headers = {"apiKey": os.environ.get("IDF_API_KEY_1")}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    pprint(data)

    # Création d’une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Ajout des polygones isochrones
    for feature, time in zip(data.get("isochrones", []), TIMES_RANGES):
        with open(
            f"/Users/mazziap/Developer/isochrone_map/isochrone_map/data/geojson_total/isochrone_metro_total_{int(time // 60)}_min",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(feature["geojson"], f)

        folium.GeoJson(
            feature["geojson"],
            style_function=lambda x: {
                "fillColor": "#3186cc",
                "color": "#3186cc",
                "weight": 2,
                "fillOpacity": 0.3,
            },
        ).add_to(m)

    m.save("isochrone_transport_paris.html")
    print("✅ Carte générée : isochrone_transport_paris.html")
else:
    print("Erreur :", response.status_code, response.text)
