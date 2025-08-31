from typing import List, Dict, Any


import folium


def _color_ramp(n: int) -> List[str]:
    """Palette simple du plus court (clair) au plus long (foncé)."""
    # Sélection de couleurs lisibles sans config de style spécifique
    base = [
        "#cfe8ff",  # 1
        "#9fd0ff",  # 2
        "#6fb8ff",  # 3
        "#3fa0ff",  # 4
        "#0f88ff",  # 5
        "#006fe6",  # 6
        "#0056b3",  # 7
    ]
    if n <= len(base):
        return base[:n]
    # Si plus de 7, répéter graduellement
    extra = []
    for i in range(n - len(base)):
        extra.append(base[-1])
    return base + extra


# ------------- RENDU FOLIUM -------------


def render_folium_map(
    geojson: Dict[str, Any],
    lat: float,
    lon: float,
    minutes: List[int],
    out_html: str = "isochrones_map.html",
) -> None:
    m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)
    folium.Marker([lat, lon], tooltip="Point de départ").add_to(m)

    # Ordonner du plus long au plus court pour que le court soit au-dessus
    feats = sorted(
        geojson["features"], key=lambda f: f["properties"].get("value", 0), reverse=True
    )

    colors = _color_ramp(len(feats))
    for idx, feat in enumerate(feats):
        minutes_val = int(round(feat["properties"].get("value", 0) / 60))
        gj = folium.GeoJson(
            data=feat,
            name=f"{minutes_val} min",
            style_function=lambda x, c=colors[idx]: {
                "fillColor": c,
                "color": c,
                "weight": 1,
                "fillOpacity": 0.45,
            },
            highlight_function=lambda x: {"weight": 2, "fillOpacity": 0.6},
            tooltip=folium.GeoJsonTooltip(fields=[], aliases=[], sticky=False),
        )
        gj.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    m.save(out_html)
