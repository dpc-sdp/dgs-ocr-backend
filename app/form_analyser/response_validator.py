
from utils.logger_util import LoggerUtil
from form_analyser.field_builder import FieldBuilder
from form_analyser.enums.field_validation import FieldValidation
from form_analyser.enums.field_parser import FieldParser
from form_analyser.enums.cover_types import CoverTypes
from form_analyser.liability_builder import LiabilityBuilder


class ResponseValidator:

    logger = LoggerUtil("ResponseStructure")

    def __init__(self, fields: dict, coverType: CoverTypes) -> None:
        self.fields: dict = fields
        self.coverType: CoverTypes = coverType

    def _get(self, field_name, default_value=None):
        return self.fields.get(field_name, default_value)

    def build_response(self, request_id):

        builder = FieldBuilder(request_id)\
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
            .add_field('u_cover_start_date', self._get('u_cover_start_time'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.TIME])\
            .add_field('u_cover_end_date', self._get('u_cover_end_date'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('u_cover_end_date', self._get('u_cover_end_time'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.TIME])\
            .add_field('u_geographical_cover', self._get('u_geographical_cover'),
                       validations=[FieldValidation.REQUIRED])\

        if self.coverType is not None and self.coverType is not CoverTypes.NONE:

            coverTypes = {'value': self.coverType.value, 'raw_value': self.coverType.value,
                          'raw_value_type': 'string', 'confidence': 0.99}
            builder.add_field('u_cover_type', coverTypes,
                              validations=[FieldValidation.REQUIRED])

            amount, amount_aggregate = LiabilityBuilder(coverType=self.coverType, fields=self.fields)\
                .extract_liability()

            builder.add_field('u_liability', amount, validations=[FieldValidation.REQUIRED], parser=[FieldParser.CURRENCY]) \
                .add_field('u_liability_aggregate', amount_aggregate, validations=[FieldValidation.REQUIRED], parser=[FieldParser.CURRENCY])

        else:
            print("No cover type selected")
            self.generate_liability(
                builder=builder, coverType=CoverTypes.PUBLIC)
            self.generate_liability(
                builder=builder, coverType=CoverTypes.PRODUCT)
            self.generate_liability(
                builder=builder, coverType=CoverTypes.PROFESSIONAL)

        response = builder.build()

        return response

    def generate_liability(self, builder, coverType):
        amount, amount_aggregate = LiabilityBuilder(coverType=coverType, fields=self.fields)\
            .extract_liability()

        builder.add_field('u_'+coverType.value+'_liability', amount, validations=[FieldValidation.REQUIRED], parser=[FieldParser.CURRENCY]) \
            .add_field('u_'+coverType.value+'_liability_aggregate', amount_aggregate, validations=[FieldValidation.REQUIRED], parser=[FieldParser.CURRENCY])
