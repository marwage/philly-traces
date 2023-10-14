import json
import pprint

import numpy as np


def to_hours(sec: float):
    return sec / 3600


def pick_job(jobs: list):
    np.random.seed(42)
    indices = np.random.randint(0, len(jobs), size=3)

    for idx in indices:
        jo = jobs[idx]
        print(f"Job index: {idx}")
        pprint.pprint(jo)

        start_time = jo["mw_start_time"]
        print(f"start time: {to_hours(start_time)}")
        runtime = jo["mw_end_time"] - start_time
        print(f"runtime: {to_hours(runtime)}")

        if "scale_up" in jo:
            scale_ups = jo["scale_up"]
            for j, su in enumerate(scale_ups):
                scale_ups[j] = to_hours(su - start_time)
            print(f"scale ups: {scale_ups}")
        else:
            print("no scale ups")

        if "scale_down" in jo:
            scale_downs = jo["scale_down"]
            for j, sd in enumerate(scale_downs):
                scale_downs[j] = to_hours(sd - start_time)
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
        print("---")


def main():
    with open("jobs_executed_stretch16.json", "r") as json_file:
        jobs = json.load(json_file)
    pick_job(jobs)


if __name__ == "__main__":
    main()
