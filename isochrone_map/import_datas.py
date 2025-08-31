import json
import requests
import os

from isochrone_map.constants import MP_DATA_LAT, MP_DATA_LONG, TOTAL_LAT, TOTAL_LONG
from dotenv import load_dotenv


load_dotenv()  # charge le .env

slot = "mp_data"

if slot == "total":
    LONG = TOTAL_LONG
    LAT = TOTAL_LAT

elif slot == "mp_data":
    LONG = MP_DATA_LONG
    LAT = MP_DATA_LAT

TIMES_RANGES = [300 * i for i in range(1, 11)]

url = (
    "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/isochrones/isochrones"
)

params = {
    "to": f"{LONG};{LAT}",
    "boundary_duration[]": TIMES_RANGES,
    # "first_section_mode[]": "walking",
    "forbidden_uris[]": [
        "physical_mode:Tramway",
        "physical_mode:Bus",
        "physical_mode:Bike",
        "physical_mode:BikeSharingService",
    ],
    "datetime": "2025-09-01T08:00:00",
    "traveler_type": "fast_walker",
}
headers = {"apiKey": os.environ.get("IDF_API_KEY_2")}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()

    # Ajout des polygones isochrones
    for feature, time in zip(data.get("isochrones", []), TIMES_RANGES):
        list_coordinates = [
            [list_coordinate[0]]
            for list_coordinate in feature["geojson"]["coordinates"]
        ]

        feature["geojson"]["coordinates"] = list_coordinates

        with open(
            f"/Users/mazziap/Developer/isochrone_map/isochrone_map/data/geojson_{slot}/isochrone_metro_{slot}_{int(time // 60)}.geojson",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(feature["geojson"], f)

else:
    print("Erreur :", response.status_code, response.text)
