from math import log2
from utils.weight_patterns.base_patterns import all_zero, all_one
from utils.weight_patterns.one_hot_patterns import one_hot
from utils.weight_patterns.clear_one_patterns import clear_one, explicit_last_zero
from config.config import FAULT_TYPE_SAF, FAULT_TYPE_BRIDGE


class FourStageDetectionAlgorithm:
    """
    Five-stage detection algorithm.

    The algorithm controls:
      - how many stages
      - which input patterns per stage
      - which weight patterns per stage
      - how to interpret the outputs

    Stages:
      1. SA1 on R1   (input [1,0],  all-zero weights)
      2. SA1 on R2   (input [0,1],  all-zero weights)
      3. SA0 on R1   (input [1,0],  all-one weights)
      4. SA0 on R2   (input [0,1],  all-one weights)
      5. Bridging R1<->R2 (inputs [00,01,10,11], special weights)
    """

    def __init__(self, bit_width: int):
        self.bit_width = bit_width

        # cache base patterns (single vectors)
        self._all_zero = all_zero(bit_width)[0]      # [0,...,0]
        self._all_one = all_one(bit_width)[0]        # [1,...,1]
        
        self.detected_faults = {
            "SA1": 0,
            "SA0": 0,
            "UNKNOWN": 0
        }

    # ------------------------------------------------------------------
    # Stage control API (used by main_engine)
    # ------------------------------------------------------------------
    def get_required_stages(self) -> int:
        """Total number of stages."""
        return 4

    def get_stage_patterns(self, stage_id: int):
        """
        Return list of input patterns (each [in_R1, in_R2]) for a stage.
        """
        if stage_id == 1:
            return [[1, 0]]          # SA1, R1 active
        if stage_id == 2:
            return [[0, 1]]          # SA1, R2 active
        if stage_id == 3:
            return [[1, 0]]          # SA0, R1 active
        if stage_id == 4:
            return [[0, 1]]          # SA0, R2 active
        
        raise ValueError(f"Unknown stage_id {stage_id}")

    def get_stage_weights(self, stage_id: int):
        """
        Return (row1_weights, row2_weights) bit-vectors for a stage.
        Both returned as *logical* weights (no fault).
        """
        if stage_id in (1, 2):
            # SA1: all-zero weights on both rows
            return self._all_zero, self._all_zero
        if stage_id in (3, 4):
            # SA0: all-one weights on both rows
            return self._all_one, self._all_one
        
        raise ValueError(f"Unknown stage_id {stage_id}")

    def observe(self, stage_id, in_patterns, outputs):
            """
            Called by main_engine.
            Uses your existing analyze_stage_output() internally.
            Also updates detected_fault counters automatically.
            """

            result = self.analyze_stage_output(stage_id, in_patterns, outputs)

            if result["detected"]:
                ftype = result["fault_type"]

                if ftype == "SA1":
                    self._increment_fault_counter("SA1")

                elif ftype == "SA0":
                    self._increment_fault_counter("SA0")

                
                else:
                    self._increment_fault_counter("UNKNOWN")

            return result    

    # ------------------------------------------------------------------
    # Output analysis API (used by main_engine).
    #
    # in_patterns: list of input bit pairs [[r1_in, r2_in], ...]
    # outputs:     list of sums (same length)
    #
    # Returns:
    #   dict {
    #       "detected": bool,
    #       "fault_type": str or None,
    #       "location": str or None,
    #       "reason": str
    #   }
    # ------------------------------------------------------------------
    def analyze_stage_output(self, stage_id: int, in_patterns, outputs):
        if stage_id in (1, 2):
            
            return self._analyze_SA1(stage_id, in_patterns[0], outputs[0])

        if stage_id in (3, 4):
            
            return self._analyze_SA0(stage_id, in_patterns[0], outputs[0])

        return self._no_fault("Unknown stage in FourStageDetectionAlgorithm")

    # ------------------------------------------------------------------
    # Internal helpers: SA1, SA0, Bridging
    # ------------------------------------------------------------------
    def _analyze_SA1(self, stage_id, in_bits, output_sum):
        """
        SA1 detection:
          - weights are all-zero
          - a single SA1 at bit k gives sum = 2^k
        Only one SA1 per stage is assumed.
        """
        if output_sum == 0:
            return self._no_fault(f"Stage{stage_id}: SA1 normal (sum=0)")

        # check power of two
        if output_sum & (output_sum - 1) != 0:
            return self._no_fault(
                f"Stage{stage_id}: sum={output_sum} not a single SA1 (non power-of-two)"
            )

        bit_idx = int(log2(output_sum))

        row = "R1" if in_bits == [1, 0] else "R2"

        return self._yes(
            "SA1",
            f"{row} weight[{bit_idx}]",
            f"Stage{stage_id}: SA1 at bit {bit_idx}"
        )

    def _analyze_SA0(self, stage_id, in_bits, observed_sum):
        """
        SA0 detection:
          - weights are all-one: expected = 2^N - 1
          - single SA0 at bit k → observed = expected - 2^k
        """
        expected = (1 << self.bit_width) - 1

        if observed_sum == expected:
            return self._no_fault(f"Stage{stage_id}: SA0 normal")

        missing = expected - observed_sum

        # must be power-of-two to be single SA0
        if missing & (missing - 1) != 0:
            return self._no_fault(
                f"Stage{stage_id}: missing={missing} not single SA0 (non power-of-two)"
            )

        bit_idx = int(log2(missing))

        row = "R1" if in_bits == [1, 0] else "R2"

        return self._yes(
            "SA0",
            f"{row} weight[{bit_idx}]",
            f"Stage{stage_id}: SA0 at bit {bit_idx}"
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------


    def _increment_fault_counter(self, key):
        if key not in self.detected_faults:
            self.detected_faults[key] = 0
        self.detected_faults[key] += 1


    def _no_fault(self, reason: str):
        return {
            "detected": False,
            "fault_type": None,
            "location": None,
            "reason": reason,
        }
    
    def _yes(self, fault_type, location, reason):
        return {
            "detected": True,
            "fault_type": fault_type,
            "location": location,
            "reason": reason
        }