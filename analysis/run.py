from trace_analysis_mw import filter_jobs, load_cluster_log, jobs_to_dict
from simulate_scheduler import simulate_scheduler
from pick_job import pick_job
from fit_scaling import fit_scaling
import pprint


def run():
    jobs = load_cluster_log()
    jobs = filter_jobs(jobs)
    jobs.sort(key=lambda x: x.submitted_time)
    jobs_dict = jobs_to_dict(jobs)
    # grid search for stretch to max scaling operations gave stretch=20
    jobs_executed = simulate_scheduler(jobs_dict, sample_every=1, stretch=20)
    fit_scaling(jobs_executed)
    # pick_job(jobs_executed)


if __name__ == "__main__":
    run()
