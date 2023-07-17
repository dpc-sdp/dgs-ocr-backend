with counts as (
     select model_id,field,
          count(1) FILTER (WHERE comparison_result = 'TP'::text) AS tp_count
        , count(1) as total
     from performance_metrics
     group by 1,2
)     


select field, 
    tp_count,
    total,
        round(counts.tp_count::numeric * 1.00 / counts.total::numeric, 2) AS accuracy
from counts
order by accuracy desc
;