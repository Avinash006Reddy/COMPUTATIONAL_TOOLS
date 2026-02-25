import math

def calculate_rocket_stage(m0_structural, mf_structural, isp, g0=9.80665):
    """Calculates Delta-V for a single stage."""
    if m0_structural <= mf_structural:
        raise ValueError("Initial mass must be greater than final mass.")
    dv = isp * g0 * math.log(m0_structural / mf_structural)
    return dv

def analyze_multistage(stages):
    """
    stages: List of dicts [{'m0': float, 'mf': float, 'isp': float}]
    from bottom (Stage 1) to top.
    """
    total_dv = 0
    upper_mass = 0
    results = []

    # Calculate from top stage down to account for carrying upper stages
    for i, stage in enumerate(reversed(stages)):
        m0_total = stage['m0'] + upper_mass
        mf_total = stage['mf'] + upper_mass
        dv = stage['isp'] * 9.80665 * math.log(m0_total / mf_total)
        
        total_dv += dv
        results.append({
            "stage": len(stages) - i,
            "effective_dv": round(dv, 2),
            "m0_total": m0_total
        })
        upper_mass = m0_total

    return total_dv, list(reversed(results))

# Example: 2-stage rocket
rocket_data = [
    {'m0': 300000, 'mf': 100000, 'isp': 300}, # Stage 1
    {'m0': 50000,  'mf': 10000,  'isp': 450}  # Stage 2
]
total, breakdown = analyze_multistage(rocket_data)
print(f"Total Delta-V: {total:.2f} m/s")
