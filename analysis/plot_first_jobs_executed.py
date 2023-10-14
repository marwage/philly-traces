import json

import matplotlib.pyplot as plt
import numpy as np


def main():
    num_jobs = 64

    with open("jobs_executed.json", "r") as json_file:
        jobs = json.load(json_file)

    fig, ax = plt.subplots()

    for i in range(num_jobs):
        jo = jobs[i]
        ax.hlines(i, jo["mw_start_time"] / 60, jo["mw_end_time"] / 60)

    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Job ID")
    fig.tight_layout()
    fig.savefig("first_jobs_executed.pdf")


if __name__ == "__main__":
    main()
