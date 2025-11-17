from .base_algorithm import BaseDetectionAlgorithm
from config.config import FAULT_TYPE_SAF, FAULT_TYPE_BRIDGE

class MajorityBasedDetector(BaseDetectionAlgorithm):
    def detect_fault(self, in_bits, weight_bits, output_sum):
        # Compute nominal sum
        weight_value = sum((1 << i) * w for i, w in enumerate(weight_bits))
        expected_sum = (in_bits[0] + in_bits[1]) * weight_value

        # Derive bitwise sum representation
        expected_bits = [int(x) for x in f"{expected_sum:b}".zfill(self.bit_width)]
        output_bits   = [int(x) for x in f"{output_sum:b}".zfill(self.bit_width)]

        mismatches = sum(e != o for e, o in zip(expected_bits, output_bits))
        if mismatches > self.bit_width // 2:
            fault_type = FAULT_TYPE_BRIDGE if in_bits[0] != in_bits[1] else FAULT_TYPE_SAF
            return {
                "detected": True,
                "fault_type": fault_type,
                "location": f"{mismatches} bits disagree",
                "reason": "Majority mismatch condition"
            }

        return {"detected": False, "fault_type": None, "location": None, "reason": "Majority consistent"}
