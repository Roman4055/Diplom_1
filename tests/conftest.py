
"""
Общие фикстуры для тестов.

Для тестов Burger используются моки (unittest.mock.Mock) —
реальные классы Bun и Ingredient в тестах Burger не нужны по заданию.

Для тестов Database используется реальный объект Database:
база содержит фиксированные данные.
"""
import pytest
from unittest.mock import Mock

from praktikum.burger import Burger
from praktikum.database import Database

from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

# Константы для моков: что вернут геттеры
MOCK_BUN_NAME = 'белый хлеб'
MOCK_BUN_PRICE = 100.0

MOCK_SAUCE_NAME = 'майонез'
MOCK_FILLING_NAME = 'курица'
MOCK_TYPE_SAUCE = 'SAUCE'
MOCK_TYPE_FILLING = 'FILLING'


@pytest.fixture
def mock_bun():
    """Мок булочки: get_name и get_price возвращают заранее заданные значения."""
    bun = Mock()
    bun.get_name.return_value = MOCK_BUN_NAME
    bun.get_price.return_value = MOCK_BUN_PRICE
    return bun


@pytest.fixture
def mock_ingredient_sauce():
    """Мок ингредиента типа SAUCE с фиксированной ценой."""
    ingredient = Mock()
    ingredient.get_name.return_value = MOCK_SAUCE_NAME
    ingredient.get_type.return_value = MOCK_TYPE_SAUCE
    ingredient.get_price.return_value = 50.0
    return ingredient


@pytest.fixture
def mock_ingredient_filling():
    """Мок ингредиента типа FILLING с фиксированной ценой."""
    ingredient = Mock()
    ingredient.get_name.return_value = MOCK_FILLING_NAME
    ingredient.get_type.return_value = MOCK_TYPE_FILLING
    ingredient.get_price.return_value = 75.0
    return ingredient


@pytest.fixture
def burger():
    """Чистый экземпляр Burger без булочки и ингредиентов."""
    return Burger()

@pytest.fixture
def database():
    """Реальный экземпляр Database с фиксированным набором данных."""
    return Database()

@pytest.fixture
def mock_database():
    """
    Мок Database для тестов main() из praktikum.py.

    Возвращает кортеж (database, buns, ingredients):
      - database — мок базы: available_buns() отдаёт 2 булки,
        available_ingredients() — 6 ингредиентов;
      - buns, ingredients — сами списки моков, чтобы тесты могли
        сверять, какие именно объекты main() передала в Burger.

    Индексы 1, 4, 3, 5 из main() валидны для списка из 6 элементов.
    """
    buns = []
    for name in ['black bun', 'white bun']:
        bun = Mock()
        bun.get_name.return_value = name
        buns.append(bun)

    ingredients = []
    data = [
        (INGREDIENT_TYPE_SAUCE, 'hot sauce'),
        (INGREDIENT_TYPE_SAUCE, 'sour cream'),
        (INGREDIENT_TYPE_SAUCE, 'chili sauce'),
        (INGREDIENT_TYPE_FILLING, 'cutlet'),
        (INGREDIENT_TYPE_FILLING, 'dinosaur'),
        (INGREDIENT_TYPE_FILLING, 'sausage'),
    ]
    for ing_type, name in data:
        ingredient = Mock()
        ingredient.get_type.return_value = ing_type
        ingredient.get_name.return_value = name
        ingredients.append(ingredient)

    database = Mock()
    database.available_buns.return_value = buns
    database.available_ingredients.return_value = ingredients

    return database, buns, ingredients
