import json
import logging
import os
from metrics import convert_imperial_to_metric, parse_unit
import typer
import yaml
import xmltodict


logger = logging.getLogger(__name__)


class NotSupportedInputException(Exception):
    pass


def autoparse(filename, data):
    if filename.endswith('.yaml'):
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError as exc:
            raise exc
    if filename.endswith('.json'):
        try:
            return json.loads(data)
        except yaml.YAMLError as exc:
            raise exc
    if filename.endswith('.xml'):
        try:
            return xmltodict.parse(data)['root']
        except yaml.YAMLError as exc:
            raise exc

    raise NotSupportedInputException(f"This input type is not supported {filename}")


def normalize_units(recipe_data):
    for ingredient in recipe_data['ingredients']:
        # delete unit key if empty..
        if 'unit' in ingredient and not ingredient['unit']:
            del ingredient['unit']
        if ingredient.get('unit'):
            unit_quantity = float(ingredient['quantity']) * parse_unit(ingredient.get('unit', ''))                                              
            metric_quantity = convert_imperial_to_metric(unit_quantity)
            if not metric_quantity:
                continue
            ingredient['quantity'], ingredient['unit'] = (round(float(metric_quantity.magnitude), 2), str(metric_quantity.units))

            

def parse_input(fullpath: str):
    with open(fullpath, 'r') as f:
        data = f.read()
        parsed = autoparse(fullpath, data)
    return parsed


def run(directory: str, output: str = "output_recipes.json", dry: bool = False):
    """This command takes directory that will be parsed and outputs JSON with recipes."""
    print(f'Start processing inputs in directory: {directory}')
    all_recipes = []
    # we can do map reduce here as well to speedup the process of processing
    # and at the end we can merge them.
    for path, _, files in os.walk(directory):
        for file in files:
            full_path = f'{path}/{file}'
            try:
                data = parse_input(full_path)
                normalize_units(data)
                all_recipes.append(data)
                print(full_path)
            except NotSupportedInputException as e:
                print(e)
    if not dry:
        with open(output, 'w') as f:
            json.dump(all_recipes, f)

    return all_recipes

if __name__ == "__main__":
    typer.run(run)
