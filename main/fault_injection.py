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

    return in_faulty, w_faulty
