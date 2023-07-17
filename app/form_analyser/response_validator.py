
from utils.logger_util import LoggerUtil
from form_analyser.field_builder import FieldBuilder
from form_analyser.enums.field_validation import FieldValidation
from form_analyser.enums.field_parser import FieldParser
from form_analyser.enums.cover_types import CoverTypes


class ResponseValidator:

    logger = LoggerUtil("ResponseStructure")

    def __init__(self, fields: dict, coverType: CoverTypes) -> None:
        self.fields: dict = fields
        self.coverType: CoverTypes = coverType

    def _get(self, field_name, default_value=None):
        return self.fields.get(field_name, default_value)

    def _validate(self, validator, field_name, default_value=None):
        field = self._get(field_name, default_value)

        return validator(field).clean()

    def build_response(self, request_id):

        coverTypes = {'value': self.coverType.value, 'raw_value': self.coverType.value,
                      'raw_value_type': 'string', 'confidence': 0.99}

        builder = FieldBuilder(request_id)\
            .add_field('u_cover_type', coverTypes,
                       validations=[FieldValidation.REQUIRED])\
            .add_field('u_insurer_name', self._get('u_insurer_name'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('u_insured_name', self._get('u_insured_name'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('u_insured_abn', self._get('u_insured_abn'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.ABN])\
            .add_field('u_document_date', self._get('u_document_date'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('u_document_type', self._get('u_document_type'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('u_policy_number', self._get('u_policy_number'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('u_cover_start_date', self._get('u_cover_start_date'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('u_cover_end_date', self._get('u_cover_end_date'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('u_geographical_cover', self._get('u_geographical_cover'),
                       validations=[FieldValidation.REQUIRED])\

        self.logger.debug(f"{self.coverType} type selected")

        amount = None
        amount_aggregate = None

        if self.coverType == CoverTypes.PRODUCT:
            amount = self._get('product_amount')
            self.logger.debug(f"amount: {amount}")

            if amount is None:
                self.logger.debug(
                    "amount is empty, checking product and public amount")
                amount = self._get('public_product_amount')
                self.logger.debug(f"public_product_amount: {amount}")

            amount_aggregate = self._get('product_amount_aggregate')
            self.logger.debug(f"amount_aggregate: {amount_aggregate}")

        elif self.coverType == CoverTypes.PUBLIC:
            amount = self._get('public_amount')
            self.logger.debug(f"amount: {amount}")

            if amount is None:
                self.logger.debug(
                    "amount is empty, checking product and public amount")
                amount = self._get('public_product_amount')
                self.logger.debug(f"public_product_amount: {amount}")

            amount_aggregate = self._get('public_amount_aggregate')
            self.logger.debug(f"amount_aggregate: {amount_aggregate}")

        elif self.coverType == CoverTypes.PROFESSIONAL:
            amount = self._get('professional_amount')
            self.logger.debug(f"amount: {amount}")

            amount_aggregate = self._get('professional_amount_aggregate')
            self.logger.debug(f"amount_aggregate: {amount_aggregate}")

        else:
            self.logger.error("Unknown cover type")

        builder.add_field('u_liability', amount, validations=[FieldValidation.REQUIRED], parser=[FieldParser.CURRENCY]) \
            .add_field('u_liability_aggregate', amount_aggregate, validations=[FieldValidation.REQUIRED], parser=[FieldParser.CURRENCY])

        response = builder.build()

        return response
