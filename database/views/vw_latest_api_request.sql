create or replace VIEW vw_latest_api_request AS  
SELECT subquery.max_created_date,
    subquery.request_id,
    subquery.file_name,
    subquery.model_id,
    subquery.cover_type
   FROM ( SELECT max(api_requests.created_on) AS max_created_date,
            api_requests.request_id,
            api_requests.file_name,
            api_requests.model_id,
            api_requests.cover_type,
            row_number() OVER (PARTITION BY api_requests.file_name, api_requests.model_id, api_requests.cover_type ORDER BY (max(api_requests.created_on)) DESC) AS row_num
           FROM api_requests
          WHERE api_requests.agent = 'curl'::bpchar
          GROUP BY api_requests.request_id, api_requests.file_name, api_requests.model_id, api_requests.cover_type) subquery
  WHERE subquery.row_num = 1;
