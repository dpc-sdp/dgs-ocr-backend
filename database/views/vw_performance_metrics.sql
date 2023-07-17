create or replace VIEW performance_metrics AS  

SELECT 
	vw_transform_expected_fields.doc_name,
	vw_latest_api_request.cover_type,
    vw_field_data_set.field_key AS field,
    vw_latest_api_request.model_id,
    btrim(vw_field_data_set.value) AS predicted_value,
    vw_field_data_set.raw_value,
    btrim(vw_transform_expected_fields.field_value::text) AS expected_value,
        CASE
            WHEN lower(btrim(vw_field_data_set.value)) = lower(btrim(vw_transform_expected_fields.field_value::text)) OR 
            SIMILARITY("left"(lower(btrim(vw_field_data_set.value)), 255), "left"(lower(btrim(vw_transform_expected_fields.field_value::text)), 255)) >= .4 OR 
            lower(vw_transform_expected_fields.field_value) LIKE '%' || lower(vw_field_data_set.value) || '%' OR
            lower(vw_field_data_set.value) LIKE '%' || lower(vw_transform_expected_fields.field_value) || '%' OR
            lower(vw_field_data_set.value) IS NULL AND lower(vw_transform_expected_fields.field_value) IS NULL THEN 'TP'::text
            ELSE 'FN'::text
        END AS comparison_result,
    vw_field_data_set.confidence,
    SIMILARITY("left"(lower(btrim(vw_field_data_set.value)), 255), "left"(lower(btrim(vw_transform_expected_fields.field_value::text)), 255)) AS levenshtein_int
   FROM vw_field_data_set
     LEFT JOIN vw_latest_api_request ON 
        vw_latest_api_request.request_id = vw_field_data_set.request_id 
        AND vw_latest_api_request.model_id = vw_field_data_set.model_id
     JOIN vw_transform_expected_fields ON 
        concat(btrim(vw_transform_expected_fields.doc_name::text), '.png') = btrim(vw_latest_api_request.file_name::text) 
        AND vw_transform_expected_fields.mapped_field_name = vw_field_data_set.field_key;

