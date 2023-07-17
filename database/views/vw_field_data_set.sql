CREATE VIEW vw_field_data_set AS  WITH raw AS (
         SELECT api_response.request_id,
            api_response.model_id,
            api_response.created_on,
            api_response.expected_fields
           FROM api_response
        ), keys AS (
         SELECT raw.request_id,
            raw.model_id,
            raw.created_on,
            raw.expected_fields,
            field_key.field_key
           FROM raw,
            LATERAL json_object_keys(raw.expected_fields) field_key(field_key)
        ), key_result_set AS (
         SELECT keys.request_id,
            keys.model_id,
            keys.created_on,
            keys.expected_fields,
            keys.field_key,
            keys.expected_fields -> keys.field_key AS result_set
           FROM keys
        )
 SELECT key_result_set.request_id,
    key_result_set.model_id,
    key_result_set.created_on,
    key_result_set.expected_fields,
    key_result_set.field_key,
    key_result_set.result_set,
    key_result_set.result_set ->> 'value'::text AS value,
    key_result_set.result_set ->> 'raw_value'::text AS raw_value,
    key_result_set.result_set ->> 'confidence'::text AS confidence,
    key_result_set.result_set ->> 'raw_value_type'::text AS data_type,
    json_array_length(key_result_set.result_set -> 'parsers'::text) AS parsers,
    json_array_length(key_result_set.result_set -> 'validations'::text) AS validations
   FROM key_result_set;

