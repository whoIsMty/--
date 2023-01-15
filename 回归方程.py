import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys

def get_liner_regression_equation(x, y):
    x = np.array(x)
    y = np.array(y)
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
    x = open("1.txt","r",encoding="utf-8").readlines()[:]
    x_ =[float(line.strip().split("\t")[0]) for line in x]
    y_ =[float(line.strip().split("\t")[1]) for line in x]

    a,b,_ = get_liner_regression_equation(x_,y_)
    print(a,b)

    plt.scatter(x_, y_, c="r")
    x1, y1 = (x_, [a * x__ + b for x__ in x_])
    plt.plot(x1, y1, c="b")
    plt.show()

