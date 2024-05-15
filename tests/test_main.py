from pathlib import Path
from main import run


def test_recipes():

    result_recipies = run("tests/samples/sample_recipe", dry=True)

    assert result_recipies, "Recipe result should not be empty"
    assert len(result_recipies) == 1, "Should have 1 recipe in output"

    recipe = result_recipies[0]

    assert recipe['name'] == 'rice'
    assert recipe.get('ingredients'), 'Recipe should have "ingredients" attribute'

    ingredients = recipe['ingredients']

    assert len(ingredients) == 2

    assert ingredients[0]['item'] == 'rice'
    assert ingredients[0]['quantity'] == 199.58
    assert ingredients[0]['unit'] == 'gram'

    assert ingredients[1]['item'] == 'carrot'
    assert ingredients[1]['quantity'] == 2
    assert not ingredients[1].get('unit'), f'{ingredients[1]["item"]} should not have unit'


def test_recipe_output():
    run('tests/samples/sample_recipe')
    path = Path('output_recipes.json')
    assert path.is_file(), "output_recipes.json file should be created as a result"


def test_recipe_custom_output():

    result_recipies = run('tests/samples/sample_recipe', output='my_output.json')
    assert result_recipies
    path = Path('my_output.json')
    assert path.is_file(), "my_output.json file should be created as a result"

