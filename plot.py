columns = [
    "benchmark", "name_before", "qubits_before", "gates_before", "tcount_before", 
    "clifford_before", "twoqubit_before", "cnot_before", "had_before", 
    "measurement_before", "other_before", "depth_before", "depth_cz_before", 
    "name_after", "qubits_after", "gates_after", "tcount_after", "clifford_after", 
    "twoqubit_after", "cnot_after", "had_after", "measurement_after", "other_after", 
    "depth_after", "depth_cz_after", "method", "spider_simp", "id_simp", "pivot_simp", 
    "lcomp_simp", "pivot_gadget_simp", "gadget_simp", "time_full_reduce", 
    "time_phase_block_optimize"
]

result_file = "results.csv"

import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv(result_file, names=columns, skiprows=1)
    
    # compare the number of gates before and after optimization
    # plot the result of a bar plot, where x is the benchmark and y is the number of gates
    # before and after optimization (in two different colors)
    x = df["benchmark"]
    y1 = df["gates_before"]
    y2 = df["gates_after"]

    bar_width = 0.35
    index = range(len(x))

    fig, ax = plt.subplots(figsize=(12, 6))  # Make the figure wider
    bar1 = ax.bar(index, y1, bar_width, label='Gates Before')
    bar2 = ax.bar([i + bar_width for i in index], y2, bar_width, label='Gates After')

    ax.set_xlabel('Benchmark')
    ax.set_ylabel('Number of Gates')
    ax.set_title('Number of Gates Before and After Optimization')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(x, rotation=45)  # Rotate x labels by 45 degrees
    ax.legend()

    # Label the improvements
    for i in index:
        # Calculate the improvement, in percentage
        improvement = round((y1[i] - y2[i]) / y1[i] * 100, 2)
        ax.text(i + bar_width / 2, max(y1[i], y2[i]) + 5, f'{improvement}', ha='center')

    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()