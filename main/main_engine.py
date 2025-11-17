from config.config import *
from config.config import BRIDGE_TYPES_ACTIVE
from main.fault_classes import Fault
from main.fault_coverage_calculator import calculate_fault_coverage
from main.fault_injection import inject_fault
'''
from algorithms.weighted_sum_detector import WeightedSumDetector
from algorithms.parity_based_detector import ParityBasedDetector
from algorithms.majority_based_detector import MajorityBasedDetector
from algorithms.five_stage_detection_algorithm import FiveStageDetectionAlgorithm
from utils.weight_patterns.generator import WeightPatternGenerator
'''

def main_engine(bit_width, algo, verbose=True):

    # -----------------------------
    # Helper: weighted sum
    # -----------------------------
    def row_value(bits):
        return sum((bits[i] << i) for i in range(bit_width))

    # -----------------------------
    # Fault generation
    # -----------------------------
    fault_list = []

    # SAF faults
    for row in (1, 2):
        for bit in range(bit_width):
            fault_list.append(Fault(FAULT_TYPE_SAF, (row, bit), 0))
            fault_list.append(Fault(FAULT_TYPE_SAF, (row, bit), 1))

    # Bridging faults
    for bt in BRIDGE_TYPES_ACTIVE:
        fault_list.append(Fault(FAULT_TYPE_BRIDGE, i=0, j=1, bridge_type=bt))

    print(f"\nRunning algorithm '{algo.__class__.__name__}' (bit_width={bit_width})...")

    # -----------------------------
    # Main simulation loop
    # -----------------------------
    total_stages = algo.get_required_stages()

    for f in fault_list:

        detected = False

        # Let the algorithm control stages
        for stage_id in range(1, total_stages + 1):

            # Algorithm controls all patterns & weights
            in_patterns = algo.get_stage_patterns(stage_id)
            row1_nom, row2_nom = algo.get_stage_weights(stage_id)

            stage_outputs = []

            # Hardware simulation for each input pattern
            for in_bits in in_patterns:

                # inject fault into each row
                in_f1, w_f1 = inject_fault(in_bits, row1_nom, f, row_id=1, verbose=False)
                in_f2, w_f2 = inject_fault(in_bits, row2_nom, f, row_id=2, verbose=False)

                # compute weighted sum (hardware)
                out_sum = (in_f1[0] * row_value(w_f1)) + \
                          (in_f2[1] * row_value(w_f2))

                # collect stage output
                stage_outputs.append(out_sum)

            # give all outputs to algorithm
            result = algo.observe(stage_id, in_patterns, stage_outputs)

            if result["detected"]:
                f.detected = True
                f.detect_pattern = {"stage": stage_id, "patterns": in_patterns}
                detected = True
                break

        if verbose:
            if detected:
                print(f"→ Detected {f}")
            else:
                print(f"→ Undetected {f}")

    # -----------------------------
    # Fault coverage report
    # -----------------------------
    return calculate_fault_coverage(fault_list)