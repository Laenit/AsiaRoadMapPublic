def format_duration_hm(hours):
    h = int(hours)
    m = int(round((hours - h) * 60))
    return f"{h}h{m:02d}"
