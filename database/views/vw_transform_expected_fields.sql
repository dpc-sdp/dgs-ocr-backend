create or replace  VIEW vw_transform_expected_fields AS  
SELECT 
    vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_document_date'::text AS column_name,
    vw_expected_fields.u_document_date AS field_value,
    'u_document_date'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
SELECT 
    vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_insurer_name'::text AS column_name,
    vw_expected_fields.u_insurer_name AS field_value,
    'u_insurer_name'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_insured_name'::text AS column_name,
    vw_expected_fields.u_insured_name AS field_value,
    'u_insured_name'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_insured_abn'::text AS column_name,
    vw_expected_fields.u_insured_abn AS field_value,
    'u_insured_abn'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_policy_number'::text AS column_name,
    vw_expected_fields.u_policy_number AS field_value,
    'u_policy_number'::text AS mapped_field_name
   FROM vw_expected_fields
 
UNION ALL

 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_cover_start_date'::text AS column_name,
    vw_expected_fields.u_cover_start_date AS field_value,
    'u_cover_start_date'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_cover_end_date'::text AS column_name,
    vw_expected_fields.u_cover_end_date AS field_value,
    'u_cover_end_date'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_liability_aggregate'::text AS column_name,
    vw_expected_fields.u_liability_aggregate AS field_value,
    'u_liability_aggregate'::text AS mapped_field_name
   FROM vw_expected_fields
UNION ALL
 SELECT vw_expected_fields.id,
    vw_expected_fields.request_id,
    vw_expected_fields.agent,
    vw_expected_fields.created_on,
    vw_expected_fields.file_name,
    vw_expected_fields.doc_name,
    vw_expected_fields.cover_type,
    'u_liability'::text AS column_name,
    vw_expected_fields.u_liability AS field_value,
    'u_liability'::text AS mapped_field_name
   FROM vw_expected_fields
