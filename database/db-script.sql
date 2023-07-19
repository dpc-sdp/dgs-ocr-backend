CREATE TABLE "api_response" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "request_id" VARCHAR(50) NULL,
  "model_id" VARCHAR(50) NULL,
  "cover_type" VARCHAR(50) NULL,
  "created_on" timestamp NOT NULL,
  "expected_fields" json NULL,
  "extraction_stats" json NULL,
  "custom_model_analysis" json NULL,
  "raw_from_formrecognizer" json NULL
);

CREATE TABLE "api_response_stats" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "request_id" VARCHAR(50) NULL,
  "created_on" timestamp NOT NULL,
  "field_name" VARCHAR(50) NULL,
  "confidence" VARCHAR(50) NULL,
  "f_value" VARCHAR(255) NULL,
  "is_value_blank" VARCHAR(50) NULL,
  "is_failed_to_parse" VARCHAR(50) NULL,
  "servicenow_feedback" VARCHAR(50) NULL
);

CREATE TABLE "api_requests" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "request_id" VARCHAR(50) NULL,
  "created_by" VARCHAR(50) NULL,
  "agent" VARCHAR(50) NULL,
  "created_on" timestamp NOT NULL,
  "cover_type" VARCHAR(50) NULL,
  "file_name" VARCHAR(255) NULL,
  "file_size" VARCHAR(50) NULL,
  "preserve_artefacts" VARCHAR(50) NULL,
  "model_id" VARCHAR(50) NULL,
  "sample_result" VARCHAR(50) NULL,
  "file_stash_location" VARCHAR(255) NULL,
  "response_stash_location" VARCHAR(255) NULL
);


CREATE TABLE "expected_results" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "request_id" VARCHAR(50) NULL,
  "agent" VARCHAR(50) NULL,
  "created_on" timestamp NOT NULL,
  "file_name" VARCHAR(100) NULL,
  "doc_name" VARCHAR(100) NULL,
  "insurer_name" VARCHAR(100) NULL,
  "insurer_names" VARCHAR(100) NULL,
  "document_issue_date" VARCHAR(100) NULL,
  "insurer_abn" VARCHAR(100) NULL,
  "policy_no" VARCHAR(100) NULL,
  "professional" VARCHAR(100) NULL,
  "public" VARCHAR(100) NULL,
  "product" VARCHAR(100) NULL,
  "policy_start_date" VARCHAR(100) NULL,
  "policy_end_date" VARCHAR(100) NULL,
  "policy_currency" VARCHAR(100) NULL,
  "professional_liability_amount" VARCHAR(100) NULL,
  "professional_aggregate" VARCHAR(100) NULL,
  "public_liability_amount" VARCHAR(100) NULL,
  "product_liability_amount" VARCHAR(100) NULL,
  "product_aggregate" VARCHAR(100) NULL,
  "region" VARCHAR(100) NULL
);
