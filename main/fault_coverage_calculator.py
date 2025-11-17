def calculate_fault_coverage(fault_list):
    total = len(fault_list)
    detected = sum(1 for f in fault_list if f.detected)
    coverage = detected / total if total > 0 else 0

    saf_faults = [f for f in fault_list if f.fault_type == "SAF"]
    bridge_faults = [f for f in fault_list if f.fault_type == "BRIDGE"]

    saf_cov = sum(1 for f in saf_faults if f.detected) / len(saf_faults) if saf_faults else 0
    bridge_cov = sum(1 for f in bridge_faults if f.detected) / len(bridge_faults) if bridge_faults else 0

    print(f"\n=== Fault Coverage Summary ===")
    print(f"  Total coverage: {coverage*100:.2f}% ({detected}/{total})")
    print(f"  SAF coverage:   {saf_cov*100:.2f}% ({sum(1 for f in saf_faults if f.detected)}/{len(saf_faults)})")
    print(f"  Bridge coverage:{bridge_cov*100:.2f}% ({sum(1 for f in bridge_faults if f.detected)}/{len(bridge_faults)})")

    return {
        "total": coverage,
        "SAF": saf_cov,
        "BRIDGE": bridge_cov
    }
