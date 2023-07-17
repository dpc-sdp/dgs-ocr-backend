with counts as (
     
     select model_id,doc_name,
          count(1) FILTER (WHERE comparison_result = 'TP'::text) AS tp_count
        , count(1) as total
     from performance_metrics
     group by 1,2
--     where predicted_value is not null
--     and expected_value is not null
--     and predicted_value != expected_value
--     and levenshtein_int >0
--     and field not in ('Policy Period From', 'Policy Period To')
--     order by levenshtein_int 
--     limit 100 
)     


select model_id, doc_name, 
    tp_count,
    total,
        round(counts.tp_count::numeric * 1.00 / counts.total::numeric, 2) AS accuracy
from counts
order by accuracy desc;