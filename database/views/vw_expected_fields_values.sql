create or replace view vw_expected_fields as 

SELECT 
    	expected_results.id,
    	expected_results.request_id,
    	expected_results.agent,
    	expected_results.created_on,
    	expected_results.file_name,
    	expected_results.doc_name,
        'professional' AS cover_type,
        document_issue_date AS u_document_date,
        insurer_name AS u_insurer_name,
        insurer_names AS u_insured_name,
        insurer_abn AS u_insured_abn,
        policy_no AS u_policy_number,
        policy_start_date AS u_cover_start_date,
        policy_end_date AS u_cover_end_date,
        professional_liability_amount AS u_liability,
        professional_aggregate AS u_liability_aggregate
FROM expected_results
WHERE btrim(professional) = 'yes'

UNION ALL

SELECT 
    	expected_results.id,
    	expected_results.request_id,
    	expected_results.agent,
    	expected_results.created_on,
    	expected_results.file_name,
    	expected_results.doc_name,
        'public' AS cover_type,
        document_issue_date AS u_document_date,
        insurer_name AS u_insurer_name,
        insurer_names AS u_insured_name,
        insurer_abn AS u_insured_abn,
        policy_no AS u_policy_number,
        policy_start_date AS u_cover_start_date,
        policy_end_date AS u_cover_end_date,
        professional_liability_amount AS u_liability,
        professional_aggregate AS u_liability_aggregate
FROM expected_results
WHERE btrim(public) = 'yes'

UNION ALL

SELECT 
    	expected_results.id,
    	expected_results.request_id,
    	expected_results.agent,
    	expected_results.created_on,
    	expected_results.file_name,
    	expected_results.doc_name,
        'product' AS cover_type,
        document_issue_date AS u_document_date,
        insurer_name AS u_insurer_name,
        insurer_names AS u_insured_name,
        insurer_abn AS u_insured_abn,
        policy_no AS u_policy_number,
        policy_start_date AS u_cover_start_date,
        policy_end_date AS u_cover_end_date,
        professional_liability_amount AS u_liability,
        professional_aggregate AS u_liability_aggregate
FROM expected_results
WHERE btrim(product) = 'yes'