import datetime
import json

import matplotlib.pyplot as plt
import numpy as np
import scipy

DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"


def main():
    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)

    arrivals = []
    for jo in jobs:
        arr_date = datetime.datetime.strptime(jo["submitted_time"],
                                              DATE_FORMAT_STR)
        arr_time = arr_date.timestamp()
        arrivals.append(arr_time)

    arrivals.sort()
    fir = arrivals[0]
    arr_shifted = []
    for arr in arrivals:
        shif = arr - fir
        arr_shifted.append(shif)

    arr_diffs = []
    for i in range(1, len(arr_shifted)):
        diff = arr_shifted[i] - arr_shifted[i - 1]
        arr_diffs.append(diff)

    arr_diffs_min = []
    for arr in arr_diffs:
        diff_min = arr / 60
        arr_diffs_min.append(diff_min)

    mean = np.mean(arr_diffs_min)
    print(f"mean in min {mean}")
    std = np.std(arr_diffs_min)
    print(f"std in min {std}")

    dist = scipy.stats.poisson
    res = scipy.stats.fit(dist, arr_diffs_min, bounds={"mu": [0, 10 * mean]})
    mu = res.params.mu
    print(f"mu {mu}")

    dist = scipy.stats.expon
    res = scipy.stats.fit(dist,
                          arr_diffs_min,
                          bounds={"scale": [0, 10 * mean]})
    loc = res.params.loc
    scale = res.params.scale
    print(f"loc {loc}")
    print(f"lambda {1/scale}")

    fig, ax = plt.subplots()
    num_bins = int(1e5)
    ax.hist(arr_diffs, num_bins, density=True)

    x = np.arange(10 * mean)
    #  y = scipy.stats.poisson.pmf(x, mu)
    #  ax.plot(x, y, label="poisson")

    y = scipy.stats.expon.pdf(x, loc=loc, scale=scale)
    ax.plot(x, y, label="expon")

    ax.set_xlabel("Inter arrival times (min)")
    ax.set_ylabel("Probability")
    ax.set_xlim(left=0, right=2 * mean)
    ax.legend()
    fig.tight_layout()
    fig.savefig("arrival_times.pdf")


if __name__ == "__main__":
    main()
