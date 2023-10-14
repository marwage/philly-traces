import json

import numpy as np


def find_max_num_gpus():
    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)

    num_gpus = [j["num_gpus"] for j in jobs]
    print(np.max(num_gpus))


if __name__ == "__main__":
    find_max_num_gpus()
