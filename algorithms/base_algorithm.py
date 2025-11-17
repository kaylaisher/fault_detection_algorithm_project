

class BaseDetectionAlgorithm:
    def __init__(self, bit_width):
        self.bit_width = bit_width
        self.detected_saf = 0

    def detect_fault(self, *args, **kwargs):
        raise NotImplementedError

    def get_required_stages(self):
        raise NotImplementedError

    def get_weight_patterns(self):
        raise NotImplementedError
