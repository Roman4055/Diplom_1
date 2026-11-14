"""Юнит-тесты класса Ingredient — реальные объекты без моков."""
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import (INGREDIENT_TYPE_SAUCE,
                                        INGREDIENT_TYPE_FILLING)


class TestIngredient:

    def test_get_type_returns_type(self):
        # Подготовка: ингредиент типа SAUCE
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, 'кетчуп', 15.0)

        # Проверка: get_type возвращает переданный тип
        assert ingredient.get_type() == INGREDIENT_TYPE_SAUCE

    def test_get_name_returns_name(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, 'лук', 10.0)

        assert ingredient.get_name() == 'лук'

    def test_get_price_returns_price(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, 'лук', 10.0)

        assert ingredient.get_price() == 10.0
