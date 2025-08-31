import json
from isochrone_map.constants import (
    ISOCHRONE_MAP,
    MINUTES_RANGES,
    MP_DATA_LAT,
    MP_DATA_LONG,
    PATH_BIKING_GEO,
    PROFILE_BIKING,
    RELOAD_GEO_JSON,
)
from isochrone_map.utils.utils_bike import isochrones_with_ors
from isochrone_map.utils.utils_folium import render_folium_map


def main():
    if RELOAD_GEO_JSON:
        print("Generating GEOJSON with ORS...")
        geojson = isochrones_with_ors(
            MP_DATA_LAT, MP_DATA_LONG, MINUTES_RANGES, profile=PROFILE_BIKING
        )

        # Sauvegarder GeoJSON brut
        with open(PATH_BIKING_GEO, "w", encoding="utf-8") as f:
            json.dump(geojson, f)

    else:
        print("Loading GEOJSON...")

        with open(PATH_BIKING_GEO, "r", encoding="utf-8") as f:
            geojson = json.load(f)

    print("Rendering the map...")
    render_folium_map(
        geojson, MP_DATA_LAT, MP_DATA_LONG, MINUTES_RANGES, out_html=ISOCHRONE_MAP
    )


if __name__ == "__main__":
    main()
