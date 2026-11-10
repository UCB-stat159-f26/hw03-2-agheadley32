"""Plot a player's career matches in the style of the NYT age-difference chart."""

import matplotlib.pyplot as plt

COLORS = {"win": "#78C8E5", "loss": "#7F417C"}


def plot_career_matches(matches):
    """Scatter each match by player age vs. age difference, colored by result.

    Takes the data frame returned by get_career_matches and returns the figure.
    """
    name = matches["player"].iloc[0]
    fig, ax = plt.subplots(figsize=(10, 6))
    for result, group in matches.groupby("result"):
        ax.scatter(group["player_age"], group["age_diff"],
                   color=COLORS[result], label=result, s=10)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_title(f"{name}'s Professional Matches")
    ax.set_xlabel(f"{name}'s age")
    ax.set_ylabel("Age difference (player minus opponent, years)")
    ax.legend()
    return fig