import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from adjustText import adjust_text


def clean_data(df, col):
    df = df[pd.to_numeric(df[col], errors="coerce").notnull()]
    df[col] = pd.to_numeric(df[col])
    return df


def map_values(row, val):
    return val[row]


def read_data(url):
    df = pd.read_csv(url.replace("/edit#gid=", "/export?format=csv&gid="))
    df = df.drop(df.columns[4], axis=1)
    df = clean_data(df, "count")
    df = clean_data(df, "y")
    colours = ["magenta", "cyan", "darkmagenta", "darkcyan"]
    cluster_num = list(set(df.cluster))
    val_dict = dict(zip(cluster_num, colours))
    df["colours"] = df.cluster.apply(map_values, args=(val_dict,))
    df = df.drop_duplicates(subset=["area", "keyword"])
    list_sort = ["area", "cluster", "cluster_name", "count"]
    sort_order = [True, True, True, False]
    cols = df.columns.tolist()
    cols_ = cols[:4] + cols[5:7]
    cols_.append(cols[4])
    cols_.append(cols[-1])
    df = df.reindex(columns=cols_)

    return df.sort_values(by=list_sort, ascending=sort_order)


def label_point(x, y, val, ax):
    data = pd.concat({"x": x, "y": y, "val": val}, axis=1)
    ax.axis("off")
    for i, point in data.iterrows():
        texts = [ax.text(point["x"], point["y"], str(point["val"]))]
        adjust_text(texts)


def plot_scatter(df, area):
    df = df.rename(columns={"cluster_name": "Кластеры"})
    plt.figure(figsize=(25, 15))
    df_area = df[df.area == area]
    scatter = sns.scatterplot(
        x="x", y="y", hue="Кластеры", data=df_area, size="count", sizes=(50, 500)
    )

    h, l = scatter.get_legend_handles_labels()

    plt.legend(
        h[:5], l[:5], bbox_to_anchor=(1.15, 0.8), loc=2, borderaxespad=0.0, fontsize=24
    )
    plt.figtext(
        0.85,
        0.05,
        f"Area: {area}",
        ha="left",
        fontsize=24,
        bbox={"alpha": 0.0, "pad": 5},
    )

    label_point(df_area.x, df_area.y, df_area.keyword, plt.gca())
