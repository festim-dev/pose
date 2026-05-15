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

    df = pd.DataFrame(all_data)

    df["city_full"] = df.apply(
        lambda row: (
            float("nan")
            if pd.isna(row["city"])
            else ", ".join(
                [
                    str(x)
                    for x in [row.get("city"), row.get("region"), row.get("country")]
                    if pd.notna(x) and str(x).strip()
                ]
            )
        ),
        axis=1,
    )

    return df
