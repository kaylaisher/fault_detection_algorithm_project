from config.config import *
from config.config import BRIDGE_TYPES_ACTIVE
from main.fault_classes import Fault, Pattern
from main.fault_coverage_calculator import calculate_fault_coverage
from main.fault_injection import inject_fault
from algorithms.weighted_sum_detector import WeightedSumDetector
from algorithms.parity_based_detector import ParityBasedDetector
from algorithms.majority_based_detector import MajorityBasedDetector


def main_engine(bit_width, algorithm_name, verbose=True):
    # Select algorithm
    if algorithm_name == "weighted_sum":
        algo = WeightedSumDetector(bit_width)
    elif algorithm_name == "parity_based":
        algo = ParityBasedDetector(bit_width)
    elif algorithm_name == "majority_based":
        algo = MajorityBasedDetector(bit_width)
    else:
        raise ValueError(f"Unknown algorithm '{algorithm_name}'")

   # --- Fault generation ---
    fault_list = []
    for row in [1, 2]:
        for bit in range(bit_width):
            fault_list.append(Fault(FAULT_TYPE_SAF, (row, bit), 0))
            fault_list.append(Fault(FAULT_TYPE_SAF, (row, bit), 1))
    
    for bt in BRIDGE_TYPES_ACTIVE:
        fault_list.append(Fault(FAULT_TYPE_BRIDGE, i=0, j=1, bridge_type=bt))

    # --- Simulation setup ---
    in_patterns = [[0,0], [0,1], [1,0], [1,1]]
    row1_weights = [1 if i % 2 else 0 for i in range(bit_width)]
    row2_weights = [0 if i == 0 else 1 for i in range(bit_width)]

    print(f"\nRunning {algorithm_name} detection (bit_width={bit_width})...")
    for f in fault_list:
        detected = False
        for pat in in_patterns:
            # Inject fault for each row separately
            in_faulty1, w_faulty1 = inject_fault(pat, row1_weights, f, row_id=1, verbose=verbose)
            in_faulty2, w_faulty2 = inject_fault(pat, row2_weights, f, row_id=2, verbose=verbose)

            # Nominal + faulty output sums
            wval1_nom = sum((1 << i) * w for i, w in enumerate(row1_weights))
            wval2_nom = sum((1 << i) * w for i, w in enumerate(row2_weights))
            total_nom = (pat[0] * wval1_nom) + (pat[1] * wval2_nom)

            wval1_f = sum((1 << i) * w for i, w in enumerate(w_faulty1))
            wval2_f = sum((1 << i) * w for i, w in enumerate(w_faulty2))
            total_faulty = (in_faulty1[0] * wval1_f) + (in_faulty2[1] * wval2_f)

            result = algo.detect_fault(pat, row1_weights, total_faulty)
            if result["detected"]:
                f.detected = True
                f.detect_pattern = pat
                detected = True
                if verbose:
                    print(f"→ Detected {f} on pattern {pat}")
                break  # stop once detected

        if not detected and verbose:
            print(f"→ Undetected: {f}")

    # --- Coverage report ---
    coverage_summary = calculate_fault_coverage(fault_list)
    return coverage_summary
