import os
import warnings

import geopandas as gpd
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Photon
from shapely.geometry import Point

_geolocator = Photon(user_agent="festim-pose-metrics", timeout=10)
_geocode = RateLimiter(
    _geolocator.geocode, min_delay_seconds=1, max_retries=2, swallow_exceptions=True
)


def _geocode_cities(cities):
    """Geocode cities one at a time, never hanging and never raising.

    Cities that cannot be resolved get an empty geometry and a warning, so a
    flaky geocoding service degrades the map instead of breaking the build.
    """
    geometries, failed = [], []
    for city in cities:
        loc = _geocode(city)
        if loc is None:
            failed.append(city)
            geometries.append(None)
        else:
            geometries.append(Point(loc.longitude, loc.latitude))
    if failed:
        warnings.warn(f"Could not geocode {len(failed)} location(s): {sorted(failed)}")
    return gpd.GeoDataFrame(
        {"city": list(cities)}, geometry=geometries, crs="EPSG:4326"
    )


def find_locations_from_cache(df, filename: str, update_cache=True):
    # load cache
    if os.path.exists(filename):
        cache = gpd.read_file(filename)
    else:
        print(f"No cache found at {filename}, starting with an empty cache.")
        cache = gpd.GeoDataFrame(columns=["city", "geometry"], crs="EPSG:4326")

    cities_found = set(df["city_full"]) & set(cache["city"])
    locations_found = cache[cache["city"].isin(cities_found)]

    # for cities not found in cache, geocode and add to cache
    locs_not_found = set(df["city_full"]) - set(cache["city"])
    if locs_not_found:
        print(f"Locations not found in cache: {locs_not_found}")
        locs_new = _geocode_cities(sorted(locs_not_found))

    locations = (
        pd.concat([locations_found, locs_new], ignore_index=True)
        if locs_not_found
        else locations_found
    )

    # ensure locations matches the order of df and avoid dtype mismatch errors
    merge_df = df[["city_full"]].copy()
    merge_df["city"] = merge_df["city_full"].astype(str)
    locations["city"] = locations["city"].astype(str)
    locations = merge_df.merge(locations, on="city", how="left")
    locations = gpd.GeoDataFrame(locations, geometry="geometry")

    if update_cache and locs_not_found:
        # make sure to keep the same order as the original df
        # only cache successful lookups, so failures are retried next time
        cache["city"] = cache["city"].astype(str)
        resolved = locs_new[~locs_new.geometry.isna()].copy()
        resolved["city"] = resolved["city"].astype(str)
        cache = pd.concat([cache, resolved], ignore_index=True)
        cache.to_file(filename, driver="GeoJSON")
    return locations
