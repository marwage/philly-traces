import json

import numpy as np


def pick_job():
    with open("jobs_executed_stretch16.json", "r") as json_file:
        jobs = json.load(json_file)

    np.random.seed(42)
    i = np.random.randint(0, len(jobs))
    jo = jobs[i]

    print(f"Job index: {i}")
    print(jo)

    start_time = int(jo["mw_start_time"])
    print(f"start time: {start_time}")
    runtime = int(jo["mw_end_time"] - start_time)
    print(f"runtime: {runtime}")

    if "scale_up" in jo:
        scale_ups = jo["scale_up"]
        for j, su in enumerate(scale_ups):
            scale_ups[j] = int(su - start_time)
        print(f"scale ups: {scale_ups}")
    else:
        print("no scale ups")

    if "scale_down" in jo:
        scale_downs = jo["scale_down"]
        for j, sd in enumerate(scale_downs):
            scale_downs[j] = int(sd - start_time)
        print(f"scale downs: {scale_downs}")
    else:
        print("no scale downs")

    num_concurrent = 0
    for other_j in jobs:
        if (
            other_j != jo
            and other_j["mw_start_time"] < start_time < other_j["mw_end_time"]
        ):
            num_concurrent = num_concurrent + 1
    print(f"concurrent jobs at start: {num_concurrent}")


if __name__ == "__main__":
    pick_job()
