import pyzx as zx
import time

def flow1(circ: zx.Circuit, datas: dict = {}, quiet: bool = True):
    # Flow 1:
    # Full Reduce + Phase Block Optimize
    # 
    stats = zx.simplify.Stats()
    timing_data = {}
    
    try:
        g = circ.to_graph()
        now = time.time()
        zx.simplify.full_reduce(g, quiet=quiet, stats=stats)
        timing_data["time_full_reduce"] = time.time() - now
        full_reduce_data = stats.num_rewrites
        
        g.normalize()
        circ = zx.extract_circuit(g).to_basic_gates()
        now = time.time()
        circ_opt = zx.phase_block_optimize(circ, quiet=quiet).to_basic_gates()
        timing_data["time_phase_block_optimize"] = time.time() - now
    
        circ_data = {f"{key}_after": value for key, value in circ_opt.stats_dict().items()}
    except Exception as e:
        return {**datas, "error": str(e)}
    
    # t count, clifford count, cnot count
    meta_data = {"method": "flow1"}
    return {**datas, **circ_data, **meta_data, **full_reduce_data, **timing_data}

dir = "circuits/qasm"
result_file = "results.csv"
benchmarks = [
    # Arithmetic
    "adder_8",
    "rc_adder_6",

    # Barenco
    "barenco_tof_3",
    "barenco_tof_4",
    "barenco_tof_5",
    "barenco_tof_10",

    # GF
    "gf2^4_mult",
    "gf2^5_mult",
    # "gf2^6_mult",
    # "gf2^7_mult",
    # "gf2^8_mult",
    # "gf2^9_mult",
    # "gf2^10_mult",
    # "gf2^16_mult",
    # "gf2^32_mult",
    # "gf2^64_mult",
    # "gf2^128_mult",
    # "gf2^256_mult",

    # Miscellaneous
    "csla_mux_3",
    "csum_mux_9",
    # "cycle_17_3",
    "grover_5",
    "qft_4",

    # Ham
    "ham15-low",
    # "ham15-med",
    # "ham15-high",

    # HWB
    "hwb6",
    # "hwb8",
    # "hwb10",
    # "hwb11",
    # "hwb12",

    # Mod
    "mod5_4",
    # "mod_adder_1024",
    # "mod_adder_1048576",
    # "mod_mult_55",
    # "mod_red_21",

    # QCLA
    "qcla_adder_10",
    "qcla_com_7",
    "qcla_mod_7",

    # TOF
    "tof_3",
    "tof_4",
    "tof_5",
    "tof_10",
]

def main():
    import os
    import pandas as pd
    
    # give a warining if the result file already exists
    if os.path.exists(result_file):
        print(f"Warning: {result_file} already exists, remove it before running a new experiment.")
        exit(1)

    exp_datas = []
    # Read circuit from QASM
    for benchmark in benchmarks:
        circ = zx.Circuit.from_qasm_file(os.path.join(dir, benchmark+".qasm")).to_basic_gates()
        circ_data = {f"{key}_before": value for key, value in circ.stats_dict().items()}
        meta_data = {"benchmark": benchmark, **circ_data}
        exp_datas += [flow1(circ, meta_data)]
        pd.DataFrame(exp_datas).to_csv(result_file, index=False)

if __name__ == "__main__":
    main()