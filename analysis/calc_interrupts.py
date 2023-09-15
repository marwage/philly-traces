import datetime
import json

DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"


def count_interrupts(jo1, jobs):
    interrupts = 0
    for att1 in jo1["attempts"]:
        start1 = datetime.datetime.strptime(att1["start_time"],
                                            DATE_FORMAT_STR)
        end1 = datetime.datetime.strptime(att1["end_time"], DATE_FORMAT_STR)
        for jo2 in jobs:
            if jo1 == jo2:
                continue
            for att2 in jo2["attempts"]:
                start2 = datetime.datetime.strptime(att2["start_time"],
                                                    DATE_FORMAT_STR)
                end2 = datetime.datetime.strptime(att2["end_time"],
                                                  DATE_FORMAT_STR)
                if start1 < start2 < end1:
                    interrupts = interrupts + 1
                if start1 < end2 < end1:
                    interrupts = interrupts + 1
    return interrupts


def main():
    with open("jobs.json", "r") as json_file:
        jobs = json.load(json_file)

    interrupts = {}
    for job in jobs:
        interrupts[job["id"]] = count_interrupts(job, jobs)

    with open("interrupts.json", "w") as json_file:
        json.dump(interrupts, json_file, indent=4)


if __name__ == "__main__":
    main()
