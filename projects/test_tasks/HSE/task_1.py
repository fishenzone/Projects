import numpy as np
import pandas as pd
from funk import read_data


df = read_data(
    "https://docs.google.com/spreadsheets/d/165sp-lWd1L4qWxggw25DJo_njOCvzdUjAd414NSE8co/edit#gid=1439079331"
)

df.to_csv("task_1.csv", index=False)
