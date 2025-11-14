class BaseDetectionAlgorithm:
    def __init__(self, bit_width):
        self.bit_width = bit_width

    def detect_fault(self, in_bits, weight_bits, output_sum):
        """
        Args:
            in_bits     : list of 2 bits (e.g. [0,1])
            weight_bits : list of bits (e.g. [1,0,1,1,0,1])
            output_sum  : integer sum = Σ(in_i * weight_value)

        Returns:
            dict {
                "detected": bool,
                "fault_type": str or None,
                "location": str or None,
                "reason": str (optional)
            }
        """
        raise NotImplementedError
