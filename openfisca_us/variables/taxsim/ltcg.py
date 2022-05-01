from openfisca_us.model_api import *


class ltcg(Variable):
    value_type = float
    entity = TaxUnit
    label = "Long-term capital gains"
    unit = "currency-USD"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return add(tax_unit, period, ["long_term_capital_gains"])