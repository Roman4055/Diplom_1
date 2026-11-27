"""
Юнит-тесты класса Database.

Класс Database имитирует базу данных бургерной:
  - в __init__ заполняет списки булок и ингредиентов фиксированными данными;
  - available_buns() возвращает список булок;
  - available_ingredients() возвращает список ингредиентов.

Тесты написаны на РЕАЛЬНЫХ объектах (без моков): содержимое базы
фиксировано, поэтому ожидаемые значения можно задать явно.
Проверяем типы, количество, порядок элементов, названия, цены
и типы ингредиентов.
"""
import pytest

from praktikum.database import Database
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


# ---------------------------------------------------------------
# 1. Инициализация объекта
# ---------------------------------------------------------------
class TestDatabaseInit:
    """Тесты конструктора: база должна заполняться корректными данными."""

    def test_buns_count(self, database):
        # Подготовка: база создана фикстурой database (см. conftest.py)
        # Проверка: в базе ровно 3 булки
        assert len(database.buns) == 3

    def test_ingredients_count(self, database):
        # Проверка: в базе ровно 6 ингредиентов (3 соуса + 3 начинки)
        assert len(database.ingredients) == 6

    def test_all_buns_are_bun_instances(self, database):
        # Проверка: каждый элемент списка булок — объект класса Bun
        for bun in database.buns:
            assert isinstance(bun, Bun)

    def test_all_ingredients_are_ingredient_instances(self, database):
        # Проверка: каждый элемент списка ингредиентов — объект Ingredient
        for ingredient in database.ingredients:
            assert isinstance(ingredient, Ingredient)

    def test_buns_names_and_prices(self, database):
        # Подготовка: ожидаемые данные базы (название, цена)
        expected = [('black bun', 100), ('white bun', 200), ('red bun', 300)]

        # Проверка: названия и цены совпадают с ожидаемыми, порядок тоже
        actual = [(bun.get_name(), bun.get_price()) for bun in database.buns]
        assert actual == expected

    def test_ingredients_data(self, database):
        # Подготовка: ожидаемые данные (тип, название, цена)
        expected = [
            (INGREDIENT_TYPE_SAUCE, 'hot sauce', 100),
            (INGREDIENT_TYPE_SAUCE, 'sour cream', 200),
            (INGREDIENT_TYPE_SAUCE, 'chili sauce', 300),
            (INGREDIENT_TYPE_FILLING, 'cutlet', 100),
            (INGREDIENT_TYPE_FILLING, 'dinosaur', 200),
            (INGREDIENT_TYPE_FILLING, 'sausage', 300),
        ]

        # Проверка: тип, название и цена каждого ингредиента совпадают
        actual = [
            (ing.get_type(), ing.get_name(), ing.get_price())
            for ing in database.ingredients
        ]
        assert actual == expected


# ---------------------------------------------------------------
# 2. Метод available_buns()
# ---------------------------------------------------------------
class TestAvailableBuns:
    """Тесты метода available_buns."""

    def test_returns_list(self, database):
        # Действие: получаем список доступных булок
        buns = database.available_buns()

        # Проверка: метод вернул именно список
        assert isinstance(buns, list)

    def test_returns_all_buns(self, database):
        # Проверка: количество булок в результате совпадает с содержимым базы
        assert len(database.available_buns()) == 3

    def test_returns_same_objects_as_internal_list(self, database):
        """
        Проверка структуры: available_buns возвращает те же объекты Bun,
        которые лежат во внутреннем списке базы (а не копии с новыми данными).
        """
        # Действие: получаем список
        buns = database.available_buns()

        # Проверка: элементы совпадают с внутренним списком по названиям и ценам
        for returned, stored in zip(buns, database.buns):
            assert returned.get_name() == stored.get_name()
            assert returned.get_price() == stored.get_price()

    def test_data_matches_expected(self, database):
        # Подготовка: ожидаемые булки базы
        expected_names = ['black bun', 'white bun', 'red bun']
        expected_prices = [100, 200, 300]

        # Действие: получаем список
        buns = database.available_buns()

        # Проверка: названия и цены на своих местах, порядок сохранён
        assert [bun.get_name() for bun in buns] == expected_names
        assert [bun.get_price() for bun in buns] == expected_prices


# ---------------------------------------------------------------
# 3. Метод available_ingredients()
# ---------------------------------------------------------------
class TestAvailableIngredients:
    """Тесты метода available_ingredients."""

    def test_returns_list(self, database):
        # Действие: получаем список доступных ингредиентов
        ingredients = database.available_ingredients()

        # Проверка: метод вернул именно список
        assert isinstance(ingredients, list)

    def test_returns_all_ingredients(self, database):
        # Проверка: количество ингредиентов совпадает с содержимым базы
        assert len(database.available_ingredients()) == 6

    def test_sauces_and_fillings_present(self, database):
        """
        Проверка наполнения базы: должны быть ингредиенты обоих типов —
        3 соуса и 3 начинки.
        """
        # Действие: получаем список и считаем типы
        ingredients = database.available_ingredients()
        types = [ing.get_type() for ing in ingredients]

        # Проверка: по 3 ингредиента каждого типа
        assert types.count(INGREDIENT_TYPE_SAUCE) == 3
        assert types.count(INGREDIENT_TYPE_FILLING) == 3

    def test_ingredients_names_and_prices(self, database):
        # Подготовка: ожидаемые названия и цены в порядке добавления в базу
        expected = [
            ('hot sauce', 100),
            ('sour cream', 200),
            ('chili sauce', 300),
            ('cutlet', 100),
            ('dinosaur', 200),
            ('sausage', 300),
        ]

        # Действие: получаем список
        ingredients = database.available_ingredients()

        # Проверка: данные совпадают, порядок сохранён
        actual = [(ing.get_name(), ing.get_price()) for ing in ingredients]
        assert actual == expected

