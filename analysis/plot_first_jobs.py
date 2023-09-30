import datetime
import json

import matplotlib.pyplot as plt
import numpy as np


def main():
    DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

    num_jobs = 128

    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)

    for jo in jobs:
        arr_date = datetime.datetime.strptime(jo["submitted_time"],
                                              DATE_FORMAT_STR)
        arr_time = arr_date.timestamp()
        jo["submitted_time"] = arr_time

    jobs = sorted(jobs, key=lambda x: x["submitted_time"])

    jo_zero_sub = jobs[0]["submitted_time"]
    for jo in jobs:
        jo["submitted_time"] = jo["submitted_time"] - jo_zero_sub
        jo["submitted_time"] = jo["submitted_time"] / 60

    fig, ax = plt.subplots()

    for i in range(num_jobs):
        jo = jobs[i]
        ax.hlines(i, jo["submitted_time"],
                  jo["submitted_time"] + jo["runtime"])

    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Job ID")
    fig.tight_layout()
    fig.savefig("first_jobs.pdf")


if __name__ == "__main__":
    main()
