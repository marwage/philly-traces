import json


def main():
    with open("jobs_executed.json", "r") as json_file:
        jobs = json.load(json_file)

    print(f"num jobs {len(jobs)}")

    jobs_with_scaling = 0
    for jo in jobs:
        if "scale_up" in jo or "scale_down" in jo:
            #  print(jo)
            jobs_with_scaling = jobs_with_scaling + 1

    print(f"jobs with scaling {jobs_with_scaling}")


if __name__ == "__main__":
    main()
