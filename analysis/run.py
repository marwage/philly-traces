from fit_runtime import fit_runtime
from fit_scaling import fit_scaling
from pick_job import pick_job
from simulate_scheduler import simulate_scheduler
from trace_analysis_mw import filter_jobs, jobs_to_dict, load_cluster_log


def run():
    jobs = load_cluster_log()
    jobs = filter_jobs(jobs)
    jobs.sort(key=lambda x: x.submitted_time)
    jobs_dict = jobs_to_dict(jobs)
    # fit_runtime(jobs_dict)
    # grid search for stretch to max scaling operations gave stretch=20
    jobs_executed = simulate_scheduler(jobs_dict, sample_every=1, stretch=20)
    # grid search for sample to max scaling operations gave sample_every=15
    # jobs_executed = simulate_scheduler(jobs_dict, sample_every=15, stretch=1)
    fit_scaling(jobs_executed, relative_runtime=True)
    pick_job(jobs_executed, 10)


if __name__ == "__main__":
    run()
