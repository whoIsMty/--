import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys

plt.rcParams['font.family'] = 'SimHei'


def get_liner_regression_equation(x, y):
    n = len(x)
    if len(x) != len(y):
        print("x,y长度不一致")
        sys.exit(1)
    sum_1 = 0
    for xi, yi in zip(x, y):
        sum_1 += xi * yi
    sum_1 = n * sum_1
    a = (sum_1 - x.sum() * y.sum()) / ((x ** 2).sum() * n - x.sum() ** 2)
    b = (y.sum() - a * x.sum()) / n

    r = (np.std(x, ddof=1) / np.std(y, ddof=1)) * a
    return a, b, r


if __name__ == "__main__":
    df = None
    for file in os.listdir("."):
        if file.endswith("xlsx"):
            df = pd.read_excel(file, index_col=None)
            break

    x = np.asarray(df.iloc[0, 1:])
    y_row_length = df.shape[0]
    for i in range(1, y_row_length):
        compound_name = df.iloc[i, 0]
        y = np.asarray(df.iloc[i, 1:])
        a, b, r = get_liner_regression_equation(x, y)
        plt.scatter(x, y, c="r")
        x1, y1 = (x, [a * x_ + b for x_ in x])
        plt.plot(x1, y1, c="r")
        plt.title(compound_name)
        a = round(a, 4)
        b = round(b, 4)
        plt.text(0.1, y.max() * 0.85, f"Y={a}X+{b}\nR2={round(r ** 2, 4)}", weight="bold", color="k")
        plt.savefig(compound_name + ".png", dpi=300, format="png")
        plt.close()
