from main.main_engine import main_engine

if __name__ == "__main__":
    print("=== Fault Detection Simulation ===")
    bit_width = int(input("Enter weight bit width (e.g. 4, 6): "))
    print("Algorithms: weighted_sum, parity_based, majority_based")
    algorithm = input("Select algorithm: ").strip()

    coverage = main_engine(bit_width, algorithm)
    print("\nSimulation finished. Fault coverage summary:")
    for k, v in coverage.items():
        print(f"  {k}: {v*100:.2f}%")
