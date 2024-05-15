from pint import UnitRegistry, DimensionalityError
from pint.errors import DimensionalityError


ureg = UnitRegistry()

imperial_to_metric = {
    'inch': 'cm',
    'foot': 'meter',
    'yard': 'meter',
    'mile': 'kilometer',
    'pound': 'gram',
    'ounce': 'gram',
    'gallon': 'liter',
    'fl. oz.': 'liter ',
    'femtoliter * ounce': 'milliliters',
    'cup': 'ml'  # Added conversion for cups
}


def parse_unit(unit_string):
    """
    Parses a unit string and returns the corresponding unit object.
    """
    return ureg.parse_expression(unit_string)


def convert_imperial_to_metric(quantity):
    """
    Convert a given quantity with an imperial unit to its respective metric unit.
    """
    units = quantity.units
    if str(units) in imperial_to_metric:
        # Convert to the respective metric unit
        try:
            return quantity.to(ureg(imperial_to_metric[str(units)]))
        except DimensionalityError as e:
            print(f'Unable to convert {str(units)} into {imperial_to_metric[str(units)]}')
            return
    else:
        return quantity  # Return the original quantity if no conversion is defined

