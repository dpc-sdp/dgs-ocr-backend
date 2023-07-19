with counts as (
     select 
          model_id,
          doc_name, 
          cover_type,
          count(1) FILTER (WHERE comparison_result = 'TP'::text) AS tp_count,
          count(1) as total
     from vw_performance_metrics
     group by 1,2,3
)     

select 
	model_id as "Model",
     cover_type as "Cover Type",
     doc_name as "Document", 
     total as "Total Extracted",
     tp_count as "Total TP",
     round(counts.tp_count::numeric * 1.00 / counts.total::numeric, 2)*100 AS accuracy
from counts
order by accuracy desc;


-- Full view of the model

with counts as (
     select 
          model_id,
          doc_name, 
          count(1) FILTER (WHERE comparison_result = 'TP'::text) AS tp_count,
          count(1) as total
     from vw_performance_metrics
     group by 1,2
)     

select 
	model_id as "Model",
     doc_name as "Document", 
     total as "Total Extracted",
     tp_count as "Total TP",
     round(counts.tp_count::numeric * 1.00 / counts.total::numeric, 2)*100 AS accuracy
from counts
order by accuracy desc;