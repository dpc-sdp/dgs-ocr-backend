select 
    *,
    round(ABS(levenshtein_int::numeric - confidence::numeric), 2) as diff
from vw_performance_metrics