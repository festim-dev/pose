import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import morethemes as mt
import numpy as np
from datetime import datetime

EMAIL = "darkj385@mit.edu"
BASE_URL = "https://api.openalex.org"

DOIS = [
    "10.1016/j.nme.2019.100709",
    "10.1016/j.ijhydene.2024.03.184",
    "10.1038/s41598-020-74844-w",
    "10.1088/1741-4326/abd95f",
    "10.1088/1741-4326/ac28b0",
    "10.1088/1741-4326/ad56a0",
    "10.1016/j.nme.2021.100984",
]

JOURNAL_ABBR = {
    "Nuclear Materials and Energy": "NME",
    "International Journal of Hydrogen Energy": "Int. J. Hydrog. Energy",
    "Nuclear Fusion": "Nucl. Fusion",
    "Scientific Reports": "Sci. Rep.",
}


def get_work(doi):
    return requests.get(f"{BASE_URL}/works/https://doi.org/{doi}?mailto={EMAIL}").json()


def get_citing_dates(doi):
    work = get_work(doi)
    bare_id = work["id"].split("/")[-1]
    citing, cursor = [], "*"
    while cursor:
        data = requests.get(
            f"{BASE_URL}/works?filter=cites:{bare_id}&select=publication_date&cursor={cursor}&mailto={EMAIL}"
        ).json()
        citing.extend(data["results"])
        cursor = data["meta"]["next_cursor"]
    surname = work["authorships"][0]["author"]["display_name"].split()[-1]
    journal = JOURNAL_ABBR.get(work["primary_location"]["source"]["display_name"],
                               work["primary_location"]["source"]["display_name"])
    pub_date = datetime.strptime(work["publication_date"], "%Y-%m-%d")
    label = f"{surname}, {journal}, {pub_date.year}"
    dates = sorted(datetime.strptime(p["publication_date"], "%Y-%m-%d") for p in citing)
    return dates, label, pub_date


def plot_cumulative_citations(dois):
    mt.set_theme("urban")
    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        color=["#f46036", "#1a4848", "#f7b000", "#aceca1", "#c9f2c7"]
    )

    all_series = sorted([get_citing_dates(doi) for doi in dois], key=lambda x: x[2])
    all_dates = sorted({d for dates, _, __ in all_series for d in dates})

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    bottom = np.zeros(len(all_dates))

    for i, (dates, label, _) in enumerate(all_series):
        counts = np.array([sum(1 for d in dates if d <= t) for t in all_dates])
        top = bottom + counts
        c = colors[i % len(colors)]
        ax.fill_between(all_dates, bottom, top, step="post", alpha=0.7, color=c, label=label)
        ax.step(all_dates, top, where="post", linewidth=1, color=c)
        bottom = top

    ax.set(xlabel="Date", ylabel="Cumulative citations", title="Cumulative citations over time")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig("cumulative_citations.png", dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_cumulative_citations(DOIS)
