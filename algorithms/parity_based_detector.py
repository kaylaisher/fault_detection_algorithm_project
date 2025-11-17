from .base_algorithm import BaseDetectionAlgorithm
from config.config import FAULT_TYPE_SAF, FAULT_TYPE_BRIDGE

class ParityBasedDetector(BaseDetectionAlgorithm):
    def detect_fault(self, in_bits, weight_bits, output_sum):
        input_parity  = in_bits[0] ^ in_bits[1]
        weight_parity = sum(weight_bits) % 2
        output_parity = output_sum % 2

        if output_parity != (input_parity ^ weight_parity):
            return {
                "detected": True,
                "fault_type": FAULT_TYPE_BRIDGE if input_parity else FAULT_TYPE_SAF,
                "location": "unknown",
                "reason": f"Parity mismatch: expected {(input_parity ^ weight_parity)}, got {output_parity}"
            }

        return {"detected": False, "fault_type": None, "location": None, "reason": "Parity consistent"}
