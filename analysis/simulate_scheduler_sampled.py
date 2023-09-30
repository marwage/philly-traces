import datetime
import json

import numpy as np


def main():
    DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

    num_gpus = 16
    min_num_gpus_job = 2  # assume that every job can run with that many GPUs
    max_num_jobs = num_gpus // min_num_gpus_job

    with open("jobs_sampled.json", "r") as json_file:
        jobs = json.load(json_file)

    jobs_submit = sorted(jobs, key=lambda x: x["submit"])

    cur_jobs = []
    for i, jo in enumerate(jobs_submit):
        jo_submit = jo["submit"]
        jo_runtime = jo["runtime"]

        # jobs finish before new jobs -> scale up
        cur_jobs = sorted(cur_jobs, key=lambda x: x["mw_end_time"])
        stop_earlier = filter(lambda x: x["mw_end_time"] < jo_submit, cur_jobs)
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
            for jo_oth in cur_jobs[i + 1:]:
                if "scale_up" in cur_jobs:
                    jo_oth["scale_up"].append(jo_stop_end)
                else:
                    jo_oth["scale_up"] = [jo_stop_end]

    with open("jobs_executed_sampled.json", "w") as json_file:
        json.dump(jobs_submit, json_file, indent=4)


if __name__ == "__main__":
    main()
