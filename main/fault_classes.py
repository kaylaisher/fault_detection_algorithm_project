from config.config import NUM_INPUTS, FAULT_TYPE_SAF, FAULT_TYPE_BRIDGE

class Fault:
    def __init__(self, fault_type, index=None, forced_value=None, i=None, j=None, bridge_type=None):
        self.fault_type     = fault_type
        self.index          = index
        self.forced_value   = forced_value
        self.i              = i
        self.j              = j
        self.bridge_type    = bridge_type
        self.detected       = False
        self.detect_pattern = None

    def __repr__(self):
        if self.fault_type == FAULT_TYPE_SAF:
            return f"SAF(index={self.index}, forced={self.forced_value})"
        else:
            return f"BRIDGE(i={self.i}, j={self.j}, type={self.bridge_type})"


class Pattern:
    def __init__(self, bits):
        assert len(bits) == NUM_INPUTS
        self.bits = bits.copy()
