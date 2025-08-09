##ap icin
# utils/normalize.py

def clamp(x, a=0.0, b=100.0):
    return max(a, min(b, x))

def minmax_scale(value, min_val, max_val):
    """Scale to 0-100 with clipping"""
    if max_val == min_val:
        return 50.0
    scaled = (value - min_val) / (max_val - min_val) * 100.0
    return clamp(scaled)

def zscore_to_0_100(z, mean=0, std=1):
    """Convert zscore to 0-100 using logistic-like squish if desired, simple mapping here"""
    # map -3..+3 z to 0..100
    if std == 0:
        return 50.0
    zc = max(-3, min(3, (z - mean) / std))
    return clamp((zc + 3) / 6.0 * 100.0)
