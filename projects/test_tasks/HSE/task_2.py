import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np
import pandas as pd
import seaborn as sns
from funk import read_data, plot_scatter

sns.set_style("white")

df = read_data(
    "https://docs.google.com/spreadsheets/d/165sp-lWd1L4qWxggw25DJo_njOCvzdUjAd414NSE8co/edit#gid=1439079331"
)

num = 0
for i in list(set(df.area)):
    plot_scatter(df, i)
    plt.savefig("images/" + i + ".png", dpi=300)
    num += 1
