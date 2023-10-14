import numpy as np
import matplotlib.pyplot as plt


def get_bin_mids(edges: np.ndarray) -> list:
    bin_mids = []
    for i in range(1, len(edges)):
        mid = (edges[i - 1] + edges[i]) / 2
        bin_mids.append(mid)

    return bin_mids


def fit_time(metric: list, metric_name: str):
    mean_metric = np.mean(metric)
    std_metric = np.std(metric)

    print(f"{metric_name} mean {mean_metric}")
    print(f"{metric_name} std {std_metric}")

    num_bins = int(1e2)
    hist, edges = np.histogram(metric, bins=num_bins, density=True)
    mids = get_bin_mids(edges)

    fig, ax = plt.subplots()

    ax.scatter(mids, hist, label="Histogram", marker="x", s=0.5)

    ax.set_xlabel("Times (sec)")
    ax.set_ylabel("Probability")
    ax.set_xlim(left=0, right=5 * mean_metric)
    plt.title(metric_name)
    # fig.tight_layout()
    fig.savefig(f"{metric_name}.pdf")


def fit_frequency(metric: list, metric_name: str):
    mean_metric = np.mean(metric)
    std_metric = np.std(metric)

    print(f"{metric_name} mean {mean_metric}")
    print(f"{metric_name} std {std_metric}")

    num_bins = int(50)
    hist, edges = np.histogram(metric, bins=num_bins, density=True)
    mids = get_bin_mids(edges)

    fig, ax = plt.subplots()

    ax.scatter(mids, hist, label="Histogram", marker="x", s=2)

    ax.set_xlabel("Frequency")
    ax.set_ylabel("Probability")
    ax.set_xlim(left=0, right=5 * mean_metric)
    plt.title(metric_name)
    # fig.tight_layout()
    fig.savefig(f"{metric_name}.pdf")


def fit_scaling(jobs: list):
    num_scale_ups = []
    num_scale_downs = []
    inter_scale_up_times = []
    inter_scale_down_times = []
    num_jobs_no_scale_ups = 0
    num_jobs_no_scale_downs = 0
    for jo in jobs:
        if "scale_up" in jo:
            num_scale_ups.append(len(jo["scale_up"]))
        else:
            num_scale_ups.append(0)
            num_jobs_no_scale_ups += 1
        if "scale_down" in jo:
            num_scale_downs.append(len(jo["scale_down"]))
        else:
            num_scale_downs.append(0)
            num_jobs_no_scale_downs += 1
        if "scale_up" in jo:
            for i, sca_up in enumerate(jo["scale_up"]):
                if i == 0:
                    inter_scale_up_times.append(sca_up)
                else:
                    inter_scale_up_times.append(sca_up - jo["scale_up"][i - 1])
        if "scale_down" in jo:
            for i, sca_down in enumerate(jo["scale_down"]):
                if i == 0:
                    inter_scale_down_times.append(sca_down)
                else:
                    inter_scale_down_times.append(sca_down - jo["scale_down"][i - 1])

    print(f"total number of jobs {len(jobs)}")
    print(f"num jobs with no scale ups {num_jobs_no_scale_ups}")
    print(f"num jobs with no scale downs {num_jobs_no_scale_downs}")

    fit_frequency(num_scale_ups, "num_scale_ups")
    fit_frequency(num_scale_downs, "num_scale_downs")
    fit_time(inter_scale_up_times, "inter_scale_up_times")
    fit_time(inter_scale_down_times, "inter_scale_down_times")


if __name__ == "__main__":
    pass
