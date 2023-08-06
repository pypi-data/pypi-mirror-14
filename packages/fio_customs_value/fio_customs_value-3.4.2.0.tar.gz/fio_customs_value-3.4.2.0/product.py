# -*- coding: utf-8 -*-
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Bool, Not

__all__ = ['Product']

__metaclass__ = PoolMeta


class Product:
    "Product"

    __name__ = 'product.product'

    country_of_origin = fields.Many2One(
        'country.country', 'Country of Origin',
    )
    customs_value = fields.Numeric(
        "Customs Value",
        states={
            'invisible': Bool(Eval('use_list_price_as_customs_value')),
            'required': Not(Bool(Eval('use_list_price_as_customs_value')))
        }, depends=['use_list_price_as_customs_value'],
    )

    use_list_price_as_customs_value = fields.Boolean(
        "Use List Price As Customs Value ?"
    )

    customs_value_used = fields.Function(
        fields.Numeric("Customs Value Used"),
        'get_customs_value_used'
    )

    customs_description = fields.Text(
        "Customs Description",
        states={
            'invisible': Bool(Eval("use_name_as_customs_description")),
            'required': Not(Bool(Eval("use_name_as_customs_description")))
        },
        depends=["use_name_as_customs_description"]
    )

    use_name_as_customs_description = fields.Boolean(
        "Use Name as Customs Description ?"
    )

    customs_description_used = fields.Function(
        fields.Text("Customs Description Used"),
        "get_customs_description_used"
    )

    def get_customs_description_used(self, name):
        if self.use_name_as_customs_description:
            return self.name
        return self.customs_description

    @staticmethod
    def default_use_name_as_customs_description():
        return True

    @staticmethod
    def default_use_list_price_as_customs_value():
        return True

    def get_customs_value_used(self, name):
        if self.use_list_price_as_customs_value:
            return self.list_price
        return self.customs_value
