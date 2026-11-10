import matplotlib.pyplot as plt
import pandas as pd

from tennis_career import plot_career_matches


def test_plot_career_matches_returns_labeled_figure():
    matches = pd.DataFrame({
        "player": ["Serena Williams", "Serena Williams"],
        "result": ["win", "loss"],
        "player_age": [20.0, 21.0],
        "age_diff": [1.5, -2.0],
    })
    fig = plot_career_matches(matches)
    ax = fig.axes[0]
    assert len(ax.collections) == 2
    assert "Serena Williams" in ax.get_title()
    plt.close(fig)