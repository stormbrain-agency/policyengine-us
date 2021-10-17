from openfisca_core.model_api import *
from openfisca_us.entities import *
import numpy as np


class household_id(Variable):
    value_type = float
    entity = Household
    label = u"Unique reference for this household"
    definition_period = ETERNITY


class household_weight(Variable):
    value_type = float
    entity = Household
    label = u"Household weight"
    definition_period = YEAR


class person_household_id(Variable):
    value_type = int
    entity = Person
    label = u"Unique reference for the household of this person"
    definition_period = ETERNITY


class is_household_head(Variable):
    value_type = float
    entity = Person
    label = u"Head of household"
    definition_period = ETERNITY

    def formula(person, period, parameters):
        # Use order of input (first)
        return person.household.members_position == 0


class State(Enum):
    AK = "Alaska"
    CA = "California"


class state_code(Variable):
    value_type = Enum
    possible_values = State
    default_value = State.CA
    entity = Household
    label = u"State"
    definition_period = ETERNITY


class StateGroup(Enum):
    CONTIGUOUS_US = "Contiguous US"
    AK = "Alaska"
    HI = "Hawaii"
    GU = "Guam"
    PR = "Puerto Rico"
    VI = "Virgin Islands"


class state_group(Variable):
    value_type = Enum
    possible_values = StateGroup
    default_value = StateGroup.CONTIGUOUS_US
    entity = Household
    label = u"State group"
    definition_period = ETERNITY

    def formula(household, period, parameters):
        NON_CONTIGUOUS_STATES = ("AK", "HI", "GU", "PR", "VI")
        state_code = household("state_code", period).decode_to_str()
        return where(
            np.isin(state_code, NON_CONTIGUOUS_STATES),
            StateGroup.encode(state_code).decode(),
            StateGroup.CONTIGUOUS_US,
        )
