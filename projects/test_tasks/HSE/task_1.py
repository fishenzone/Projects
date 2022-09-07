import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np
import pandas as pd


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


df = read_data(
    "https://docs.google.com/spreadsheets/d/165sp-lWd1L4qWxggw25DJo_njOCvzdUjAd414NSE8co/edit#gid=1439079331"
)
df.to_csv("task_1.csv", index=False)
