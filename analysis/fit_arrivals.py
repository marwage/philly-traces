import datetime
import json

import matplotlib.pyplot as plt
import numpy as np
import scipy

DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"


def main():
    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)

    print(f"number of jobs {len(jobs)}")

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

    mean = np.mean(arr_diffs)
    print(f"mean in sec {mean}")
    std = np.std(arr_diffs)
    print(f"std in sec {std}")

    dist = scipy.stats.expon
    res = scipy.stats.fit(dist, arr_diffs, bounds={"scale": [0, 10 * mean]})
    loc = res.params.loc
    scale = res.params.scale
    lambd = 1 / scale
    print(f"loc {loc}")
    print(f"scale {scale}")
    print(f"lambda {lambd}")

    # hist
    num_bins = int(1e5)
    hist, bin_edges = np.histogram(arr_diffs, bins=num_bins, density=True)
    bin_mids = []
    for i in range(1, len(bin_edges)):
        mid = (bin_edges[i - 1] + bin_edges[i]) / 2
        bin_mids.append(mid)

    fig, ax = plt.subplots()

    ax.scatter(bin_mids, hist, label="Histogram", marker="x", s=0.5)

    x = np.arange(10 * mean)
    #  y = scipy.stats.poisson.pmf(x, mu)
    #  ax.plot(x, y, label="poisson")

    y = scipy.stats.expon.pdf(x, loc=loc, scale=scale)
    ax.plot(x, y, label="expon", c="orange")

    ax.set_xlabel("Inter arrival times (sec)")
    ax.set_ylabel("Probability")
    ax.set_xlim(left=0, right=10 * mean)
    ax.legend()
    fig.tight_layout()
    fig.savefig("arrival_times.pdf")


if __name__ == "__main__":
    main()
