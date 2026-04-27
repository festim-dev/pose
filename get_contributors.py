import requests
from collections import defaultdict
from datetime import datetime
import os
import time
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_contributor_stats(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    else:
        print(
            "⚠️  No GITHUB_TOKEN found in environment variables. You may hit rate limits."
        )
    # Poll until we get a 200 OK
    MAX_RETRIES = 10
    for attempt in range(MAX_RETRIES):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("✅ Data ready!")
            break
        elif response.status_code == 202:
            print(
                f"⏳ Stats being computed, retrying in 3s... (attempt {attempt + 1}/{MAX_RETRIES})"
            )
            time.sleep(3)
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(response.text)
            exit(1)
    else:
        print("❌ Timed out waiting for stats. Try again later.")
        exit(1)

    contributors = response.json()

    # Map: week timestamp -> set of contributors active that week
    weekly_contributors = defaultdict(set)

    for contributor in contributors:
        login = contributor["author"]["login"]
        for week in contributor["weeks"]:
            if week["c"] > 0:  # had at least one commit this week
                weekly_contributors[week["w"]].add(login)

    # Compute cumulative unique contributors over time
    seen = set()
    timeline = []
    for week_ts in sorted(weekly_contributors.keys()):
        seen.update(weekly_contributors[week_ts])
        timeline.append(
            {
                "date": datetime.fromtimestamp(week_ts),
                "cumulative_contributors": len(seen),
            }
        )
    return timeline


if __name__ == "__main__":
    OWNER = "festim-dev"
    REPO = "festim"
    timeline = fetch_contributor_stats(OWNER, REPO)
    for entry in timeline:
        print(entry["date"], "->", entry["cumulative_contributors"])

    # # group by month
    # monthly_contributors = defaultdict(set)
    # for week_ts, contributors in weekly_contributors.items():
    #     month = datetime.utcfromtimestamp(week_ts).strftime("%Y-%m")
    #     monthly_contributors[month].update(contributors)

    # now make a cumulative graph of number of contributors
    import matplotlib.pyplot as plt

    dates = [entry["date"] for entry in timeline]
    cumulative_contributors = [entry["cumulative_contributors"] for entry in timeline]
    plt.figure()
    plt.step(dates, cumulative_contributors)
    plt.title("Cumulative Unique Contributors Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Unique Contributors")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
