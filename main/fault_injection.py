from config.config import WEIGHT_BITS

def inject_fault(in_bits, weight_bits, fault, row_id=1, verbose=False):
    """
    Apply a given fault to the inputs or weights and return the faulty copies.
    """
    in_faulty = in_bits.copy()
    w_faulty  = weight_bits.copy()

    # --- SAF: stuck-at fault on a specific weight bit ---
    if fault.fault_type == "SAF":
        f_row, f_bit = fault.index
        if f_row == row_id:
            old_val = w_faulty[f_bit]
            w_faulty[f_bit] = fault.forced_value
            if verbose:
                print(f"[SAF] Row {f_row}, Bit {f_bit}: {old_val} → {fault.forced_value}")

    # --- BRIDGE: between input[0] and input[1] ---
    elif fault.fault_type == "BRIDGE":
        i, j = fault.i, fault.j
        a, b = in_bits[i], in_bits[j]
        bt = fault.bridge_type

        # 0: wired-AND
        if bt == 0:  a_faulty, b_faulty = a & b, a & b
        # 1: wired-OR
        elif bt == 1:  a_faulty, b_faulty = a | b, a | b
        # 2: i dominant j
        elif bt == 2:  a_faulty, b_faulty = a, a
        # 3: i dominant-AND j
        elif bt == 3:  a_faulty, b_faulty = a, a & b
        # 4: j dominant i
        elif bt == 4:  a_faulty, b_faulty = b, b
        # 5: j dominant-AND i
        elif bt == 5:  a_faulty, b_faulty = a & b, b
        # 6: i dominant-OR j
        elif bt == 6:  a_faulty, b_faulty = a, a | b
        # 7: j dominant-OR i
        elif bt == 7:  a_faulty, b_faulty = a | b, b
        else:
            raise ValueError(f"Unknown bridge_type: {bt}")

        in_faulty[i], in_faulty[j] = a_faulty, b_faulty

        if verbose:
            print(f"[BRIDGE] {i}<->{j} type={bt} | {a,b}→{a_faulty,b_faulty}")

    elif fault.fault_type == "COUPLING":

        # Fault object fields:
        # fault.aggr_row      -> 1 or 2 (aggressor)
        # fault.aggr_bit      -> which bit
        # fault.victim_bit    -> victim bit index (case 1..N)
        # fault.transition    -> "0->1" or "1->0"
        # fault.prev_bits     -> previous R1[] or R2[] (list)
        # fault.curr_bits     -> current R1[] or R2[] (list)

        ag = fault.aggr_row
        ab = fault.aggr_bit
        vb = fault.victim_bit

        prev = fault.prev_bits[ab]
        curr = fault.curr_bits[ab]

        # Check if the aggressor matches the transition condition
        if fault.transition == "0->1" and prev == 0 and curr == 1:
            triggered = True
        elif fault.transition == "1->0" and prev == 1 and curr == 0:
            triggered = True
        else:
            triggered = False

        if triggered:

            # If ROW 1 triggered → affect ROW 2
            if ag == 1 and row_id == 2:
                old = w_faulty[vb]
                w_faulty[vb] = 1 - w_faulty[vb]   # invert
                if verbose:
                    print(f"[COUPLING R1 {fault.transition}] R2[{vb}]: {old}→{w_faulty[vb]}")

            # If ROW 2 triggered → affect ROW 1
            elif ag == 2 and row_id == 1:
                old = w_faulty[vb]
                w_faulty[vb] = 1 - w_faulty[vb]
                if verbose:
                    print(f"[COUPLING R2 {fault.transition}] R1[{vb}]: {old}→{w_faulty[vb]}")


    return in_faulty, w_faulty
