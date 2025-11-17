from .base_algorithm import BaseDetectionAlgorithm
from config.config import FAULT_TYPE_SAF, FAULT_TYPE_BRIDGE

class WeightedSumDetector(BaseDetectionAlgorithm):
    def detect_fault(self, in_bits, weight_bits, output_sum):
        # Compute expected weighted sum
        weight_value = sum((1 << i) * w for i, w in enumerate(weight_bits))
        expected_sum = (in_bits[0] + in_bits[1]) * weight_value

        if output_sum != expected_sum:
            # Fault detected
            diff = output_sum - expected_sum
            if abs(diff) > (weight_value // 2):
                fault_type = FAULT_TYPE_BRIDGE
            else:
                fault_type = FAULT_TYPE_SAF
            return {
                "detected": True,
                "fault_type": fault_type,
                "location": f"sum_diff={diff}",
                "reason": f"Expected {expected_sum}, got {output_sum}"
            }

        return {"detected": False, "fault_type": None, "location": None, "reason": "No mismatch"}
