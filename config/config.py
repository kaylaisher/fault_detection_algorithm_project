# --- Simulation Parameters ---
NUM_INPUTS       = 2
NUM_WEIGHTS      = 1
WEIGHT_BITS      = 6
MAX_WEIGHT_VALUE = (1 << WEIGHT_BITS) - 1

# --- Fault Types ---
FAULT_TYPE_SAF    = "SAF"
FAULT_TYPE_BRIDGE = "BRIDGE"

# --- General Options ---
VERBOSE_DEFAULT   = True
SAVE_CSV_FILENAME = "fault_sim_results.csv"

FAULT_MODE = "BOTH"   # Controls which fault classes are generated (SAF, BRIDGE, or BOTH)

BRIDGE_TYPES_ACTIVE = list(range(8))  # Lets you limit specific bridge types for targeted experiments

NUM_ROW = 2           # Keeps future scalability in mind

RANDOM_SEED = None