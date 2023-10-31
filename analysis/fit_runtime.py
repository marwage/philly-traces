import json

import matplotlib.pyplot as plt
import numpy as np
import scipy


def dist(runtimes: [float], mean: float, std: float):
    dist = scipy.stats.norm
    res = scipy.stats.fit(
        dist, runtimes, bounds={"loc": [0, 10 * mean], "scale": [0, 10 * std]}
    )
    norm_loc = res.params.loc
    norm_scale = res.params.scale
    print(f"norm loc {norm_loc}")
    print(f"norm scale {norm_scale}")

    # expon
    dist = scipy.stats.expon
    res = scipy.stats.fit(dist, runtimes, bounds={"scale": [0, 4 * mean]})
    expon_loc = res.params.loc
    expon_scale = res.params.scale
    expon_lambda = 1 / expon_scale
    print(f"expon loc {expon_loc}")
    print(f"expon scale {expon_scale}")
    print(f"expon lambda {expon_lambda}")

    # hist
    num_bins = int(1e5)
    hist, bin_edges = np.histogram(runtimes, bins=num_bins, density=True)
    bin_mids = []
    for i in range(1, len(bin_edges)):
        mid = (bin_edges[i - 1] + bin_edges[i]) / 2
        bin_mids.append(mid)

    fig, ax = plt.subplots()

    ax.scatter(bin_mids, hist, label="Histogram", marker="x", s=0.5)

    x = np.arange(10 * mean)
    y = scipy.stats.expon.pdf(x, loc=expon_loc, scale=expon_scale)
    ax.plot(x, y, label="expon", c="orange")

    ax.set_xlabel("Job runtime (min)")
    ax.set_ylabel("Probability")
    ax.set_xlim(left=0, right=10 * mean)
    ax.legend()
    fig.tight_layout()
    fig.savefig("runtimes.pdf")


def fit_runtime(jobs: list):
    runtimes = []  # in seconds
    for jo in jobs:
        runti = jo["runtime"]
        runtimes.append(runti)
    runtimes.sort()

    # stats
    mean = np.mean(runtimes)
    print(f"runtime mean in min {mean}")
    std = np.std(runtimes)
    print(f"runtime std in min {std}")
    maxi = np.max(runtimes)
    print(f"runtime max in min {maxi}")

    rng = np.random.default_rng()
    runt = rng.choice(runtimes)
    print(f"sampled runtime in min {runt}")

    dist(runtimes, mean, std)


def main():
    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)
    fit_runtime(jobs)


if __name__ == "__main__":
    main()
