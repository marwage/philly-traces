import numpy as np


def main():
    np.random.seed(42)

    # arrival
    lambd = 0.01935871330231356
    size = 20
    arr_samp = np.random.exponential(scale=1 / lambd, size=size - 1)
    helper = [0]
    helper.extend(arr_samp)
    arr_samp = helper
    print(f"arrival samples {arr_samp}")

    # runtime
    expon_scale = 2142.2007610812907
    run_samp = np.random.exponential(scale=expon_scale, size=size)
    print(f"runtime samples {run_samp}")

    prev_start = 0
    start_end = []
    for arr, runt in zip(arr_samp, run_samp):
        start = prev_start + arr
        end = start + runt
        start_end.append((start, end))
        print(f"start {start}, end {end}")
        prev_start = prev_start + arr

    ten_start, ten_end = start_end[10 - 1]
    print(f"10th start {ten_start}")
    print(f"10th end {ten_end}")

    scale_downs = []
    scale_ups = []
    for sta, end in start_end:
        if ten_start < sta < ten_end:
            scale_downs.append(sta)
        if ten_start < end < ten_end:
            scale_ups.append(end)
    print(f"scale downs {scale_downs}")
    print(f"scale ups {scale_ups}")


if __name__ == "__main__":
    main()
