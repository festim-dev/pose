from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)


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
    )
    response = client.run_report(request)
    return response
