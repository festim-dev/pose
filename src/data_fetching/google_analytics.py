from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    Filter,
)

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


def users_city(start_date_ga, end_date_ga, property_id="YOUR-GA4-PROPERTY-ID"):
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="activeUsers")],
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
    return response


def users_world(start_date_ga, end_date_ga, property_id="YOUR-GA4-PROPERTY-ID"):
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers"), Metric(name="newUsers")],
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
    return response


def engagement_time_per_active_user(
    start_date_ga, end_date_ga, property_id="YOUR-GA4-PROPERTY-ID"
):
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="userEngagementDuration"), Metric(name="activeUsers")],
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
    return response
