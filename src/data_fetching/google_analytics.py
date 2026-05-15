from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    Filter,
)
import pandas as pd

# Data center cities to filter - ALL confirmed bots
BOT_CITIES = [
    # Original spike cities
    "Phoenix",
    "Des Moines",
    "Boydton",
    "Moses Lake",
    "Cheyenne",
    "San Jose",
    "Chicago",
    "San Antonio",
    # Other common data center cities
    "Ashburn",
    "Council Bluffs",
    "The Dalles",
    "Quincy",
]


def run_report(
    start_date_ga, end_date_ga, property_id="YOUR-GA4-PROPERTY-ID", daily=False
):
    client = BetaAnalyticsDataClient()

    dimensions = [Dimension(name="date")] if daily else []
    dimensions += [
        Dimension(name="city"),
        Dimension(name="region"),
        Dimension(name="country"),
    ]

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dimensions,
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
            Metric(name="engagementRate"),
            Metric(name="userEngagementDuration"),
        ],
        date_ranges=[
            DateRange(
                start_date=start_date_ga.strftime("%Y-%m-%d"),
                end_date=end_date_ga.strftime("%Y-%m-%d"),
            )
        ],
        dimension_filter=FilterExpression(
            not_expression=FilterExpression(
                filter=Filter(
                    field_name="city",
                    in_list_filter=Filter.InListFilter(values=BOT_CITIES),
                )
            ),
        ),
    )
    response = client.run_report(request)

    df = convert_response_to_dataframe(response)
    return df


def convert_response_to_dataframe(response) -> pd.DataFrame:
    metric_names = [m.name for m in response.metric_headers]
    dimension_names = [d.name for d in response.dimension_headers]
    data = []
    for row in response.rows:
        dim_vals = [d.value for d in row.dimension_values]
        met_vals = [float(m.value) for m in row.metric_values]
        data.append(dim_vals + met_vals)

    df = pd.DataFrame(data, columns=dimension_names + metric_names)

    # create a full city column for geocoding, handling missing values and avoiding "(not set)"
    df["city_full"] = df.apply(
        lambda row: (
            "(not set)"
            if pd.isna(row["city"]) or row["city"] == "(not set)"
            else ", ".join(
                [
                    str(x)
                    for x in [row.get("city"), row.get("region"), row.get("country")]
                    if pd.notna(x) and str(x).strip() and x != "(not set)"
                ]
            )
        ),
        axis=1,
    )
    return df
