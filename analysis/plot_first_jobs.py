import datetime
import json

import matplotlib.pyplot as plt


def plot_first_jobs():
    DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

    num_jobs = 128
    executed = True

    if executed:
        file_name = "jobs_executed.json"
    else:
        file_name = "jobs.json"
    with open(file_name, "r") as json_file:
        jobs = json.load(json_file)

    if not executed:
        for jo in jobs:
            arr_date = datetime.datetime.strptime(jo["submitted_time"], DATE_FORMAT_STR)
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
        if executed:
            ax.hlines(i, jo["mw_start_time"] / 60, jo["mw_end_time"] / 60)
        else:
            ax.hlines(i, jo["submitted_time"], jo["submitted_time"] + jo["runtime"])

    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Job ID")
    fig.tight_layout()
    fig.savefig("first_jobs.pdf")


if __name__ == "__main__":
    plot_first_jobs()
