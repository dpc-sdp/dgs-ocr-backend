with counts as (
     
     select model_id,
          count(1) FILTER (WHERE comparison_result = 'TP'::text) AS tp_count
        , count(1) as total
     from performance_metrics
     group by 1
)     


select model_id, 
    tp_count,
    total,
        round(counts.tp_count::numeric * 1.00 / counts.total::numeric, 2)*100 AS accuracy
from counts
order by accuracy desc
;