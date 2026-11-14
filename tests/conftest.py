"""
Общие фикстуры для тестов класса Burger.
Все моки создаются через unittest.mock.Mock — реальные классы
Bun и Ingredient в тестах Burger не используются по заданию.
"""
import pytest
from unittest.mock import Mock

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
    from praktikum.burger import Burger
    return Burger()
