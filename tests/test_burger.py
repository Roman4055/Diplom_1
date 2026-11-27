"""
Юнит-тесты класса Burger.

Burger — агрегатор: хранит булку и список ингредиентов, а расчёт цены
и формирование чека делегирует геттерам Bun и Ingredient. Поэтому
реальные Bun и Ingredient не нужны — используются моки.

Моки создаются фабриками make_bun и make_ingredient из tests/helpers.py
(фикстуры mock_bun / mock_ingredient_* из conftest.py здесь не
используются: фабрики дают гибкость по параметрам).

Структура:
  - позитивные тесты: init, set_buns, add/remove/move, get_price, get_receipt;
  - негативные тесты (класс TestBurgerNegative): поведение при
    некорректных данных — обращение к цене/чеку без булки, None в
    списке ингредиентов, отрицательный индекс при удалении.
"""
import pytest

from praktikum.burger import Burger

from tests.helpers import make_bun, make_ingredient


# ---------------------------------------------------------------
# 1. Инициализация
# ---------------------------------------------------------------
class TestBurgerInit:
    def test_bun_is_none_after_creation(self):
        # Шаг 1: создаём бургер без аргументов
        burger = Burger()

        # Проверка: булка не назначена (None)
        assert burger.bun is None

    def test_ingredients_list_is_empty_after_creation(self):
        # Шаг 1: создаём бургер без аргументов
        burger = Burger()

        # Проверка: список ингредиентов пуст
        assert burger.ingredients == []


# ---------------------------------------------------------------
# 2. set_buns
# ---------------------------------------------------------------
class TestSetBuns:
    def test_set_buns_assigns_bun(self):
        # Шаг 1: создаём бургер и мок-булку
        burger = Burger()
        bun = make_bun()

        # Шаг 2: назначаем булку
        burger.set_buns(bun)

        # Проверка: в бургере ровно эта булка
        assert burger.bun is bun

    def test_set_buns_overwrites_previous_bun(self):
        # Шаг 1: создаём бургер и две булки
        burger = Burger()
        first_bun = make_bun(name='первая')
        second_bun = make_bun(name='вторая')

        # Шаг 2: назначаем первую, затем вторую
        burger.set_buns(first_bun)
        burger.set_buns(second_bun)

        # Проверка: осталась последняя назначенная булка
        assert burger.bun is second_bun


# ---------------------------------------------------------------
# 3. add_ingredient
# ---------------------------------------------------------------
class TestAddIngredient:
    def test_add_ingredient_appends_to_list(self):
        # Шаг 1: создаём бургер и ингредиент
        burger = Burger()
        ingredient = make_ingredient()

        # Шаг 2: добавляем ингредиент
        burger.add_ingredient(ingredient)

        # Проверка: ингредиент оказался в списке
        assert burger.ingredients == [ingredient]

    def test_add_ingredient_preserves_order(self):
        # Шаг 1: создаём бургер и три ингредиента
        burger = Burger()
        first = make_ingredient(name='первый')
        second = make_ingredient(name='второй')
        third = make_ingredient(name='третий')

        # Шаг 2: добавляем по очереди
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.add_ingredient(third)

        # Проверка: порядок добавления сохранён
        assert burger.ingredients == [first, second, third]


# ---------------------------------------------------------------
# 4. remove_ingredient
# ---------------------------------------------------------------
class TestRemoveIngredient:
    def test_remove_ingredient_by_index(self):
        # Шаг 1: кладём два ингредиента
        burger = Burger()
        first = make_ingredient(name='первый')
        second = make_ingredient(name='второй')
        burger.add_ingredient(first)
        burger.add_ingredient(second)

        # Шаг 2: удаляем первый по индексу 0
        burger.remove_ingredient(0)

        # Проверка: остался только второй
        assert burger.ingredients == [second]

    def test_remove_ingredient_from_empty_list_raises(self):
        # Шаг 1: создаём пустой бургер
        burger = Burger()

        # Шаг 2 и проверка: удаление из пустого списка вызывает IndexError
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_remove_ingredient_invalid_index_raises(self):
        # Шаг 1: кладём один ингредиент
        burger = Burger()
        burger.add_ingredient(make_ingredient())

        # Шаг 2 и проверка: индекс за границами списка вызывает IndexError
        with pytest.raises(IndexError):
            burger.remove_ingredient(5)


# ---------------------------------------------------------------
# 5. move_ingredient
# ---------------------------------------------------------------
class TestMoveIngredient:
    def test_move_ingredient_forward(self):
        # Шаг 1: кладём три ингредиента
        burger = Burger()
        first = make_ingredient(name='первый')
        second = make_ingredient(name='второй')
        third = make_ingredient(name='третий')
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.add_ingredient(third)

        # Шаг 2: перемещаем первый на позицию 2 (вперёд)
        burger.move_ingredient(0, 2)

        # Проверка: новый порядок [второй, третий, первый]
        assert burger.ingredients == [second, third, first]

    def test_move_ingredient_backward(self):
        # Шаг 1: кладём три ингредиента
        burger = Burger()
        first = make_ingredient(name='первый')
        second = make_ingredient(name='второй')
        third = make_ingredient(name='третий')
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.add_ingredient(third)

        # Шаг 2: перемещаем третий на позицию 0 (назад)
        burger.move_ingredient(2, 0)

        # Проверка: новый порядок [третий, первый, второй]
        assert burger.ingredients == [third, first, second]

    def test_move_ingredient_to_same_index(self):
        # Шаг 1: кладём два ингредиента
        burger = Burger()
        first = make_ingredient(name='первый')
        second = make_ingredient(name='второй')
        burger.add_ingredient(first)
        burger.add_ingredient(second)

        # Шаг 2: перемещаем элемент на ту же позицию
        burger.move_ingredient(0, 0)

        # Проверка: порядок не изменился
        assert burger.ingredients == [first, second]

    def test_move_ingredient_invalid_index_raises(self):
        # Шаг 1: кладём один ингредиент
        burger = Burger()
        burger.add_ingredient(make_ingredient())

        # Шаг 2 и проверка: перемещение по несуществующему индексу
        # вызывает IndexError (pop падает раньше, чем insert)
        with pytest.raises(IndexError):
            burger.move_ingredient(5, 0)


# ---------------------------------------------------------------
# 6. get_price
# ---------------------------------------------------------------
class TestGetPrice:
    def test_price_is_bun_only(self):
        # Шаг 1: назначаем только булку за 100
        burger = Burger()
        burger.set_buns(make_bun(price=100.0))

        # Проверка: цена = цена булки * 2 (верх и низ), без ингредиентов
        assert burger.get_price() == 200.0

    def test_price_with_one_ingredient(self):
        # Шаг 1: булка 100 + ингредиент 50
        burger = Burger()
        burger.set_buns(make_bun(price=100.0))
        burger.add_ingredient(make_ingredient(price=50.0))

        # Проверка: 100 * 2 + 50 = 250
        assert burger.get_price() == 250.0

    def test_price_with_multiple_ingredients(self):
        # Шаг 1: булка 100 + ингредиенты 50 и 75
        burger = Burger()
        burger.set_buns(make_bun(price=100.0))
        burger.add_ingredient(make_ingredient(price=50.0))
        burger.add_ingredient(make_ingredient(price=75.0))

        # Проверка: 100 * 2 + 50 + 75 = 325
        assert burger.get_price() == 325.0

    def test_get_price_calls_bun_get_price_once(self):
        # Шаг 1: назначаем булку
        burger = Burger()
        bun = make_bun()
        burger.set_buns(bun)

        # Шаг 2: считаем цену
        burger.get_price()

        # Проверка: геттер цены булки вызван ровно один раз
        bun.get_price.assert_called_once_with()

    def test_get_price_calls_each_ingredient_once(self):
        # Шаг 1: булка + два ингредиента
        burger = Burger()
        burger.set_buns(make_bun())
        first = make_ingredient()
        second = make_ingredient(name='курица')
        burger.add_ingredient(first)
        burger.add_ingredient(second)

        # Шаг 2: считаем цену
        burger.get_price()

        # Проверка: геттер цены каждого ингредиента вызван ровно один раз
        first.get_price.assert_called_once_with()
        second.get_price.assert_called_once_with()

    @pytest.mark.parametrize(
        'bun_price, ingredient_prices, expected_price',
        [
            [200.0, [], 400.0],
            [150.0, [50.0], 350.0],
            [100.0, [50.0, 75.0, 25.0], 350.0],
        ],
        ids=['только булочка', 'один ингредиент', 'три ингредиента'],
    )
    def test_price_calculation_parametrized(self, bun_price, ingredient_prices, expected_price):
        # Шаг 1: собираем бургер из параметров набора
        burger = Burger()
        burger.set_buns(make_bun(price=bun_price))
        for price in ingredient_prices:
            burger.add_ingredient(make_ingredient(price=price))

        # Проверка: цена считается как булка*2 + все ингредиенты
        assert burger.get_price() == expected_price


# ---------------------------------------------------------------
# 7. get_receipt
# ---------------------------------------------------------------
class TestGetReceipt:
    def test_receipt_with_single_ingredient(self):
        # Шаг 1: булка 'белый хлеб' за 100 + один соус 'майонез' за 50
        burger = Burger()
        burger.set_buns(make_bun(name='белый хлеб', price=100.0))
        burger.add_ingredient(make_ingredient(ing_type='SAUCE', name='майонез', price=50.0))

        # Проверка: чек соответствует заданному формату
        expected = (
            '(==== белый хлеб ====)\n'
            '= sauce майонез =\n'
            '(==== белый хлеб ====)\n'
            '\n'
            'Price: 250.0'
        )
        assert burger.get_receipt() == expected

    def test_receipt_ingredient_type_is_lowercase(self):
        # Шаг 1: кладём ингредиент типа SAUCE (в верхнем регистре)
        burger = Burger()
        burger.set_buns(make_bun())
        burger.add_ingredient(make_ingredient(ing_type='SAUCE', name='майонез'))

        # Проверка: тип в чеке напечатан в нижнем регистре
        assert '= sauce майонез =' in burger.get_receipt()

    def test_receipt_price_matches_get_price(self):
        # Шаг 1: булка 100 + ингредиент 50
        burger = Burger()
        burger.set_buns(make_bun(price=100.0))
        burger.add_ingredient(make_ingredient(price=50.0))

        # Проверка: цена в чеке совпадает с get_price()
        assert f'Price: {burger.get_price()}' in burger.get_receipt()

    def test_receipt_bun_name_appears_twice(self):
        # Шаг 1: назначаем булку
        burger = Burger()
        burger.set_buns(make_bun(name='белый хлеб'))
        burger.add_ingredient(make_ingredient())

        # Проверка: название булки встречается дважды (верх и низ бургера)
        assert burger.get_receipt().count('белый хлеб') == 2

    def test_receipt_is_string(self):
        # Шаг 1: назначаем булку и ингредиент
        burger = Burger()
        burger.set_buns(make_bun())
        burger.add_ingredient(make_ingredient())

        # Проверка: чек — это строка
        assert isinstance(burger.get_receipt(), str)

    def test_receipt_ingredients_order_follows_list(self):
        # Шаг 1: кладём два ингредиента в известном порядке
        burger = Burger()
        burger.set_buns(make_bun())
        burger.add_ingredient(make_ingredient(name='майонез'))
        burger.add_ingredient(make_ingredient(ing_type='FILLING', name='курица'))
        receipt = burger.get_receipt()

        # Проверка: в чеке майонез идёт раньше курицы
        assert receipt.index('майонез') < receipt.index('курица')


# ---------------------------------------------------------------
# 8. Негативные тесты: некорректные данные
# ---------------------------------------------------------------
class TestBurgerNegative:
    """
    Проверяем поведение при нарушении контракта.

    Важно: в текущей реализации Burger не валидирует входные данные
    (в set_buns и add_ingredient можно передать что угодно). Ошибки
    проявляются не в момент добавления, а позже — при расчёте цены
    или формировании чека. Эти тесты фиксируют такое поведение
    («fail late») как задокументированный контракт класса.
    """

    def test_get_price_without_bun_raises_attribute_error(self):
        # Шаг 1: создаём бургер без булки
        burger = Burger()

        # Шаг 2 и проверка: get_price обращается к bun.get_price(),
        # а bun == None — падаем с AttributeError
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_receipt_without_bun_raises_attribute_error(self):
        # Шаг 1: создаём бургер без булки
        burger = Burger()

        # Шаг 2 и проверка: get_receipt обращается к bun.get_name(),
        # а bun == None — падаем с AttributeError
        with pytest.raises(AttributeError):
            burger.get_receipt()

    def test_get_price_with_none_ingredient_raises(self):
        # Шаг 1: валидная булка + None вместо ингредиента
        burger = Burger()
        burger.set_buns(make_bun())
        burger.add_ingredient(None)

        # Шаг 2 и проверка: get_price вызывает ingredient.get_price()
        # у None — падаем с AttributeError
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_receipt_with_none_ingredient_raises(self):
        # Шаг 1: валидная булка + None вместо ингредиента
        burger = Burger()
        burger.set_buns(make_bun())
        burger.add_ingredient(None)

        # Шаг 2 и проверка: get_receipt вызывает ingredient.get_type()
        # у None — падаем с AttributeError
        with pytest.raises(AttributeError):
            burger.get_receipt()

    def test_remove_ingredient_negative_index_removes_last(self):
        # Шаг 1: кладём два ингредиента
        burger = Burger()
        sauce = make_ingredient(name='майонез')
        filling = make_ingredient(ing_type='FILLING', name='курица')
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)

        # Шаг 2: удаляем по индексу -1
        # Особенность Python: pop(-1) — валидный вызов, удаляет
        # ПОСЛЕДНИЙ элемент, а не бросает IndexError.
        # Этот тест фиксирует такое поведение, чтобы оно не «съехало»
        # незаметно, если код метода изменится.
        burger.remove_ingredient(-1)

        # Проверка: остался только первый ингредиент (майонез)
        assert burger.ingredients == [sauce]

