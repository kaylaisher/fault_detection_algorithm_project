from main.main_engine import main_engine
from algorithms.five_stage_detection_algorithm import FiveStageDetectionAlgorithm
from algorithms.weighted_sum_detector import WeightedSumDetector
from algorithms.parity_based_detector import ParityBasedDetector
from algorithms.majority_based_detector import MajorityBasedDetector
from algorithms.four_stage_detection_algorithm import FourStageDetectionAlgorithm

if __name__ == "__main__":
    print("=== Fault Detection Simulation ===")
    bit_width = int(input("Enter weight bit width: "))
    print("Algorithms: five_stage, four_stage, weighted_sum, parity_based, majority_based")
    algo_name = input("Select algorithm: ").strip()

    if algo_name == "five_stage":
        algo = FiveStageDetectionAlgorithm(bit_width)
    elif algo_name == "four_stage":
        algo = FourStageDetectionAlgorithm(bit_width)
    elif algo_name == "weighted_sum":
        algo = WeightedSumDetector(bit_width)
    elif algo_name == "parity_based":
        algo = ParityBasedDetector(bit_width)
    elif algo_name == "majority_based":
        algo = MajorityBasedDetector(bit_width)
    else:
        raise ValueError("Unknown algorithm")

    coverage = main_engine(bit_width, algo)

    print("\nDetected Faults:")
    print(algo.detected_faults)

    print("\nCoverage Summary:")
    for k, v in coverage.items():
        print(f"  {k}: {v*100:.2f}%")
