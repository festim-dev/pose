import pandas as pd
import matplotlib.pyplot as plt

import morethemes as mt

mt.set_theme("urban")

# https://coolors.co/1a4848-f7b000-f46036-c9f2c7-aceca1
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#1a4848", "#f7b000", "#f46036", "#c9f2c7", "#aceca1"]
)

data = [
    ("2026-01-20", 3),
    ("2026-01-21", 2),
    ("2026-01-23", 3),
    ("2026-01-26", 5),
    ("2026-01-27", 9),
    ("2026-01-28", 3),
    ("2026-01-29", 3),
    ("2026-01-30", 2),
    ("2026-02-02", 1),
    ("2026-02-03", 38),
    ("2026-02-04", 2),
    ("2026-02-09", 2),
    ("2026-02-10", 3),
    ("2026-02-12", 2),
    ("2026-02-13", 1),
    ("2026-02-17", 1),
    ("2026-02-18", 10),
    ("2026-02-19", 6),
    ("2026-03-02", 5),
]

df = pd.DataFrame(data, columns=["date", "number_of_interviews"])

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date (safety, in case CSV gets modified)
df = df.sort_values("date")

# Plot
plt.figure()
plt.plot(df["date"], df["number_of_interviews"])

plt.xlabel("Date")
plt.ylabel("Number of Interviews")
plt.title("Interviews Conducted Over Time")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# cumulative plot

df["cumulative_interviews"] = df["number_of_interviews"].cumsum()

plt.figure()
plt.plot(df["date"], df["cumulative_interviews"])
plt.fill_between(
    df["date"], df["cumulative_interviews"], alpha=0.3
)  # Add area under the curve

plt.scatter(
    df["date"].iloc[-1],
    df["cumulative_interviews"].iloc[-1],
    zorder=5,
    color="C0",
    s=100,
)  # Highlight last point
plt.annotate(
    f"{df['cumulative_interviews'].iloc[-1]} Interviews",
    (df["date"].iloc[-1], df["cumulative_interviews"].iloc[-1]),
    textcoords="offset points",
    xytext=(0, 10),
    ha="center",
)

plt.xlabel("Date")
plt.title("Cumulative Interviews Conducted Over Time", loc="left")
plt.xticks(rotation=45)
plt.ylim(bottom=0)

# remove spines
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.tight_layout()

plt.savefig("interviews.svg")

plt.show()
