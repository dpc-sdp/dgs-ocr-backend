with counts as (
     select 
          model_id,
          cover_type,
          field,
          count(1) FILTER (WHERE comparison_result = 'TP'::text) AS tp_count,
          count(1) as total
     from performance_metrics
     group by 1,2,3
)     

select 
	model_id as "Model",
     cover_type as "Cover Type",
	field as "Field Name", 
     total as "Total Extracted",
     tp_count as "Total TP",
     round(counts.tp_count::numeric * 1.00 / counts.total::numeric, 2)*100 AS accuracy
from counts
order by model_id, accuracy desc;