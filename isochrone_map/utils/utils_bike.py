from __future__ import annotations

import os
from typing import List, Dict, Any

import openrouteservice as ors

from dotenv import load_dotenv


load_dotenv()  # charge le .env

# ------------- UTILS -------------


def minutes_to_ranges(minutes: List[int]) -> List[int]:
    return sorted([int(m) * 60 for m in minutes])


# ------------- ORS ENGINE -------------


def isochrones_with_ors(
    lat: float, lon: float, minutes: List[int], profile: str = "cycling-regular"
) -> Dict[str, Any]:
    if ors is None:
        raise RuntimeError(
            "Le module openrouteservice n'est pas installé. Faites: pip install openrouteservice"
        )
    api_key = os.environ.get("ORS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Définissez la variable d'environnement ORS_API_KEY avec votre clé API."
        )

    client = ors.Client(key=api_key)
    ranges_s = minutes_to_ranges(minutes)

    params = {
        "locations": [[lon, lat]],
        "profile": profile,
        "range": ranges_s,
        "interval": None,
        "location_type": "start",
        "range_type": "time",
        "attributes": ["total_pop"],
        "smoothing": 0.3,
    }
    res = client.isochrones(**params)
    return res
