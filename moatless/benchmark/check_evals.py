import json

with open("swebench_lite_all_evaluations.json", "r") as f:
    evals = json.load(f)
    import statistics

    patch_lengths = []

    for eval in evals:
        tgt_files = len(eval["expected_spans"])
        for solve in eval["resolved_by"]:
            patch_len = len(solve["patch"].split("\n"))
            patch_lengths.append(patch_len)

    if patch_lengths:
        # Calculate the 90th percentile
        percentile_90 = statistics.quantiles(patch_lengths, n=10)[8]

        # Filter out patch lengths over the 90th percentile
        filtered_patch_lengths = [
            length for length in patch_lengths if length <= percentile_90
        ]

        if filtered_patch_lengths:
            avg_patch_len = sum(filtered_patch_lengths) / len(filtered_patch_lengths)
            var_patch_len = statistics.variance(filtered_patch_lengths)
            print(f"Average patch length: {avg_patch_len}")
            print(f"Variance of patch length: {var_patch_len}")
        else:
            print("No patches found after filtering.")
    else:
        print("No patches found.")
