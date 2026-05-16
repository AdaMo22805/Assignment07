import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    return mo, pd, plt


@app.cell
def _(pd):
    df = pd.read_csv("../data/features/events.csv")
    return (df,)


@app.cell
def _(df, plt):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["duration_minutes"], bins=50, edgecolor="black")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Event Durations")
    fig
    return


if __name__ == "__main__":
    app.run()
