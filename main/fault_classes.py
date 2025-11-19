from config.config import NUM_INPUTS, FAULT_TYPE_SAF, FAULT_TYPE_BRIDGE, FAULT_TYPE_COUPLING

class Fault:
    def __init__(self,
        fault_type,
        index=None, forced_value=None,      # SAF
        i=None, j=None, bridge_type=None,   # BRIDGE
        aggr_row=None, aggr_bit=None,       # COUPLING
        victim_bit=None, transition=None,   # COUPLING
        prev_bits=None, curr_bits=None      # COUPLING
    ):
        
        # Common
        self.fault_type = fault_type
        self.detected = False
        self.detect_pattern = None

        # SAF fields
        self.index = index
        self.forced_value = forced_value

        # BRIDGE fields
        self.i = i
        self.j = j
        self.bridge_type = bridge_type

        # COUPLING fields
        self.aggr_row = aggr_row          # 1 or 2
        self.aggr_bit = aggr_bit          # aggressor bit index
        self.victim_bit = victim_bit      # victim bit index
        self.transition = transition      # "0->1" or "1->0"
        self.prev_bits = prev_bits        # full row bits BEFORE
        self.curr_bits = curr_bits        # full row bits AFTER


    def __repr__(self):
        if self.fault_type == FAULT_TYPE_SAF:
            return f"SAF(index={self.index}, forced={self.forced_value})"
        
        if self.fault_type == FAULT_TYPE_BRIDGE:
            return f"BRIDGE(i={self.i}, j={self.j}, type={self.bridge_type})"
        
        if self.fault_type == FAULT_TYPE_COUPLING:
            return (
                f"COUPLING(aggr_row={self.aggr_row}, "
                f"aggr_bit={self.aggr_bit}, victim_bit={self.victim_bit}, "
                f"transition='{self.transition}')"
            )

        return f"Fault(type={self.fault_type})"
