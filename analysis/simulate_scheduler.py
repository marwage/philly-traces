import datetime
import copy
import json

import numpy as np


def subsample(li: list, every: int):
    return li[::every]


def filter_earlier(submitted: float, jobs: list) -> list:
    return list(filter(lambda x: x["mw_end_time"] < submitted, jobs))


def validate(jobs: list):
    for jo in jobs:
        if not (jo["mw_start_time"] + jo["runtime"] == jo["mw_end_time"]):
            print("job wrong")


def simulate_scheduler(jobs: list, sample_every: int = 1, stretch: int = 1) -> list:
    assert sample_every == 1 or stretch == 1
    num_gpus = 16
    min_num_gpus_job = 2  # assume that every job can run with that many GPUs
    max_num_jobs = num_gpus // min_num_gpus_job

    jobs_executed = copy.deepcopy(jobs)
    jobs_executed.sort(key=lambda x: x["submitted_time"])
    if sample_every > 1:
        jobs_executed = subsample(jobs_executed, sample_every)

    jo_zero_sub = jobs_executed[0]["submitted_time"]
    for jo in jobs_executed:
        jo["submitted_time"] = jo["submitted_time"] - jo_zero_sub
        if stretch > 1:
            jo["submitted_time"] = jo["submitted_time"] * stretch

    cur_jobs = []
    for i, jo in enumerate(jobs_executed):
        jo_submit = jo["submitted_time"]
        jo_runtime = jo["runtime"]

        # jobs finish before new jobs -> scale up
        cur_jobs = sorted(cur_jobs, key=lambda x: x["mw_end_time"])
        stop_earlier = filter_earlier(jo_submit, cur_jobs)
        for stop_ea in stop_earlier:
            jo_stop_end = stop_ea["mw_end_time"]
            for jo_oth in cur_jobs:
                if jo_oth == stop_ea:
                    continue
                if jo_stop_end > jo_oth["mw_start_time"]:
                    jo_oth.setdefault("scale_up", [])
                    jo_oth["scale_up"].append(jo_stop_end)
            cur_jobs.remove(stop_ea)

        if len(cur_jobs) < max_num_jobs:  # resources available
            jo["mw_start_time"] = jo_submit
            jo["mw_end_time"] = jo_submit + jo_runtime

            if len(cur_jobs) > 0:  # scale down
                for cur_jo in cur_jobs:
                    cur_jo.setdefault("scale_down", [])
                    cur_jo["scale_down"].append(jo_submit)

            cur_jobs.append(jo)
        else:  # resources busy -> start delayed
            jo_first_fin = cur_jobs[0]
            jo["mw_start_time"] = jo_first_fin["mw_end_time"]
            jo["mw_end_time"] = jo_first_fin["mw_end_time"] + jo_runtime

            cur_jobs.remove(jo_first_fin)
            cur_jobs.append(jo)

    # no new jobs but scale ups
    cur_jobs = sorted(cur_jobs, key=lambda x: x["mw_end_time"])
    for i, cur_jo in enumerate(cur_jobs):
        jo_stop_end = cur_jo["mw_end_time"]
        if i + 1 < len(cur_jobs):
            for jo_oth in cur_jobs[i + 1 :]:
                if "scale_up" in cur_jobs:
                    jo_oth["scale_up"].append(jo_stop_end)
                else:
                    jo_oth["scale_up"] = [jo_stop_end]

    validate(jobs_executed)

    return jobs_executed


def main():
    DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

    sample_every = 1
    stretch_factor = 20

    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)

    for jo in jobs:
        arr_date = datetime.datetime.strptime(jo["submitted_time"], DATE_FORMAT_STR)
        jo["submitted_time"] = arr_date

    jobs_executed = simulate_scheduler(
        jobs, sample_every=sample_every, stretch=stretch_factor
    )

    if sample_every > 1:
        file_name = f"jobs_executed_subsampled{sample_every}.json"
    elif stretch_factor > 1:
        file_name = f"jobs_executed_stretch{stretch_factor}.json"
    else:
        file_name = "jobs_executed.json"
    with open(file_name, "w") as json_file:
        json.dump(jobs_executed, json_file, indent=4)


if __name__ == "__main__":
    main()
