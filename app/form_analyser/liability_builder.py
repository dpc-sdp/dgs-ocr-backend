
import re
from form_analyser.enums.cover_types import CoverTypes
from utils.logger_util import LoggerUtil
from form_analyser.services.parser_service import CurrencyParser
from form_analyser.services.response_dto import ValidationDto


class LiabilityBuilder:

    logger = LoggerUtil("LiabilityBuilder")

    def __init__(self, coverType: CoverTypes,  fields: dict):
        self.coverType = coverType
        self.fields = fields

    def extract_liability(self):
        self.logger.debug(f"{self.coverType} type selected")
        amount = None
        amount_aggregate = None
        aggregate_label = None

        if self.coverType == CoverTypes.PRODUCT:
            amount = self.get_liability(
                'product_amount', 'public_product_amount')
            amount_aggregate = self.get_liability(
                'product_amount_aggregate', 'public_product_amount_aggregate')
            aggregate_label = self.get_liability(
                'product_aggregate_label', 'public_product_aggregate_label')
            self.logger.debug(f"aggregate_label : {aggregate_label}")

            document_type = self.fields.get("u_document_type")
            if not self.is_empty(document_type):
                document_type = document_type.get("value").lower()
                if ('product' in document_type) or ('general' in document_type):
                    if self.is_empty(amount):
                        amount = self.get_liability(
                            'public_amount', 'public_product_amount')

                    if self.is_empty(amount_aggregate):
                        amount_aggregate = self.get_liability(
                            'public_amount_aggregate', 'public_product_amount_aggregate')

                    if self.is_empty(aggregate_label):
                        aggregate_label = self.get_liability(
                            'public_aggregate_label', 'public_product_aggregate_label')

            if (not self.is_empty(aggregate_label)) and (not self.is_empty(amount)) and self.is_empty(amount_aggregate):
                amount_aggregate = amount

            amount_aggregate = self.is_aggregate_lessthan_amount(
                amount, amount_aggregate)

        elif self.coverType == CoverTypes.PUBLIC:
            amount = self.get_liability(
                'public_amount', 'public_product_amount')
            amount_aggregate = self.get_liability(
                'public_amount_aggregate', 'public_product_amount_aggregate')
            aggregate_label = self.get_liability(
                'public_aggregate_label', 'public_product_aggregate_label')

            self.logger.debug(f"aggregate_label : {aggregate_label}")

            if (not self.is_empty(aggregate_label)) and (not self.is_empty(amount)) and self.is_empty(amount_aggregate):
                amount_aggregate = amount

            amount_aggregate = self.is_aggregate_lessthan_amount(
                amount, amount_aggregate)

        elif self.coverType == CoverTypes.PROFESSIONAL:
            amount = self.fields.get('professional_amount')
            self.logger.debug(f"professional_amount: {amount}")

            amount_aggregate = self.fields.get('professional_amount_aggregate')
            self.logger.debug(f"amount_aggregate: {amount_aggregate}")

            aggregate_label = self.fields.get('professional_aggregate_label')
            self.logger.debug(f"aggregate_label : {aggregate_label}")

            if (not self.is_empty(aggregate_label)) and (not self.is_empty(amount)) and self.is_empty(amount_aggregate):
                amount_aggregate = amount

            amount_aggregate = self.is_aggregate_lessthan_amount(
                amount, amount_aggregate)

        else:
            self.logger.error("Unknown cover type")

        return amount, amount_aggregate

    def is_empty(self, input):
        return input is None or input.get("value") is None or input.get("value") == ""

    def get_liability(self, amount_liability: str, joined_amount_liability: str):
        amount = self.fields.get(amount_liability)
        self.logger.debug(f"{amount_liability} : {amount}")

        if self.is_empty(amount):
            self.logger.debug(
                f"amount is empty, checking {joined_amount_liability}")
            amount = self.fields.get(joined_amount_liability)
            self.logger.debug(f"{joined_amount_liability} : {amount}")

        return amount

    def is_aggregate_lessthan_amount(self, amount, aggregate_amount):
        self.logger.debug("checking if aggregate amount is less than amount")
        if (not self.is_empty(amount)) and (not self.is_empty(aggregate_amount)):
            self.logger.debug("aggregate amount and amount are not empty")
            amt: ValidationDto = CurrencyParser().parse(amount.get("value"))
            agg_amt: ValidationDto = CurrencyParser().parse(aggregate_amount.get("value"))
            if agg_amt.output < amt.output:
                self.logger.debug("aggregate amount is less than the amount")
                return {'value': 0, 'raw_value': 0,
                        'raw_value_type': 'string', 'confidence': 0.99}

        self.logger.debug("aggregate amount or amount is empty")
        return aggregate_amount
