import requests
import pandas as pd


def get_fusion_machine_developers():
    page = 1
    while True:
        url = f"https://www.fusionenergybase.com/api/v1/organizations/?page={page}&tag=fusion-machine-developers&sort=display_name"
        response = requests.get(url)
        data = response.json()
        if data["next"] is None:
            break
        yield data
        page += 1


def get_research_organizations():
    page = 1
    while True:
        url = f"https://www.fusionenergybase.com/api/v1/organizations/?page={page}&tag=research-organizations&sort=display_name"
        response = requests.get(url)
        data = response.json()
        if data["next"] is None:
            break
        yield data
        page += 1


def aggregate_data(organization_generator):
    all_data = []
    for data in organization_generator:
        all_data.extend(data["results"])
    return pd.DataFrame(all_data)
