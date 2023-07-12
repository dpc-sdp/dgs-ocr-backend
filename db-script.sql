CREATE TABLE "api_response" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "request_id" character(50) NULL,
  "model_id" character(50) NULL,
  "created_on" timestamp NOT NULL,
  "expected_fields" json NULL,
  "extraction_stats" json NULL,
  "custom_model_analysis" json NULL,
  "raw_from_formrecognizer" json NULL
);

CREATE TABLE "api_requests" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "request_id" VARCHAR(50) NULL,
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
  "request_id" character(50) NULL,
  "agent" character(50) NULL,
  "created_on" timestamp NOT NULL,
  "file_name" character(100) NULL,
  "doc_name" character(100) NULL,
  "insurer_name" character(100) NULL,
  "insurer_names" character(100) NULL,
  "document_issue_date" character(100) NULL,
  "insurer_abn" character(100) NULL,
  "policy_no" character(100) NULL,
  "professional" character(100) NULL,
  "public" character(100) NULL,
  "product" character(100) NULL,
  "policy_start_date" character(100) NULL,
  "policy_end_date" character(100) NULL,
  "policy_currency" character(100) NULL,
  "professional_liability_amount" character(100) NULL,
  "professional_aggregate" character(100) NULL,
  "public_liability_amount" character(100) NULL,
  "product_liability_amount" character(100) NULL,
  "product_aggregate" character(100) NULL,
  "region" character(100) NULL
);
