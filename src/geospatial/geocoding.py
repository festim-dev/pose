import os
import geopandas as gpd
import pandas as pd


def find_locations_from_cache(df, filename: str, update_cache=True):
    # load cache
    if os.path.exists(filename):
        cache = gpd.read_file(filename)
    else:
        print(f"No cache found at {filename}, starting with an empty cache.")
        cache = gpd.GeoDataFrame(columns=["city", "geometry"], crs="EPSG:4326")

    cities_found = set(df["city"]) & set(cache["city"])
    locations_found = cache[cache["city"].isin(cities_found)]

    # for cities not found in cache, geocode and add to cache
    locs_not_found = set(df["city"]) - set(cache["city"])
    if locs_not_found:
        print(f"Locations not found in cache: {locs_not_found}")
        locs_new = gpd.tools.geocode(list(locs_not_found))
        locs_new["city"] = list(locs_not_found)

    locations = (
        pd.concat([locations_found, locs_new], ignore_index=True)
        if locs_not_found
        else locations_found
    )

    # ensure locations matches the order of df and avoid dtype mismatch errors
    merge_df = df[["city"]].copy()
    merge_df["city"] = merge_df["city"].astype(str)
    locations["city"] = locations["city"].astype(str)
    locations = merge_df.merge(locations, on="city", how="left")
    locations = gpd.GeoDataFrame(locations, geometry="geometry")

    if update_cache and locs_not_found:
        # make sure to keep the same order as the original df
        cache["city"] = cache["city"].astype(str)
        locs_new["city"] = locs_new["city"].astype(str)
        cache = pd.concat([cache, locs_new], ignore_index=True)
        cache.to_file(filename, driver="GeoJSON")
    return locations
