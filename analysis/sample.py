import json

import numpy as np


def main():
    np.random.seed(42)
    size = 20

    # arrival
    arr_scale = 168.23665708228316
    arr_samp = np.random.exponential(scale=arr_scale, size=size - 1)
    helper = [0]
    helper.extend(arr_samp)
    arr_samp = helper

    # runtime
    runt_scale = 19550.609413406524
    runt_samp = np.random.exponential(scale=runt_scale, size=size)

    prev_start = 0
    jobs = []
    for arr, runt in zip(arr_samp, runt_samp):
        jo = {"submit": arr, "runtime": runt}
        jobs.append(jo)
        prev_start = prev_start + arr

    with open("./jobs_sampled.json", "w") as json_file:
        json.dump(jobs, json_file, indent=4)


if __name__ == "__main__":
    main()
