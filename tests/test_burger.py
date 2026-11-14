"""
Юнит-тесты класса Burger.

Покрываются все публичные методы: __init__, set_buns,
add_ingredient, remove_ingredient, move_ingredient,
get_price, get_receipt.

Булочка и ингредиенты заменены моками (unittest.mock.Mock),
чтобы тесты Burger зависели только от логики самого Burger,
а не от реальной реализации Bun и Ingredient.
"""
import pytest
from unittest.mock import Mock

# Импортируем значения констант из conftest не требуется:
# значения передаются прямо в тесты через фикстуры.


# ---------------------------------------------------------------
# 1. Инициализация объекта
# ---------------------------------------------------------------
class TestBurgerInit:
    """Тесты конструктора: объект должен создаваться в пустом состоянии."""

    def test_bun_is_none_after_creation(self, burger):
        # Действие: создаём Burger (фикстура burger уже это сделала)
        # Проверка: булочка по умолчанию не назначена
        assert burger.bun is None

    def test_ingredients_list_is_empty_after_creation(self, burger):
        # Проверка: список ингредиентов пуст, но существует (не None)
        assert burger.ingredients == []


# ---------------------------------------------------------------
# 2. Назначение булочки
# ---------------------------------------------------------------
class TestSetBuns:
    """Тесты метода set_buns."""

    def test_set_buns_assigns_bun(self, burger, mock_bun):
        # Действие: назначаем мок-булочку
        burger.set_buns(mock_bun)

        # Проверка: атрибут bun — это ровно тот объект, который передали
        assert burger.bun is mock_bun

    def test_set_buns_overwrites_previous_bun(self, burger, mock_bun):
        # Подготовка: назначаем первую булочку
        burger.set_buns(mock_bun)
        new_bun = Mock()

        # Действие: назначаем вторую булочку поверх первой
        burger.set_buns(new_bun)

        # Проверка: осталась только последняя назначенная булочка
        assert burger.bun is new_bun


# ---------------------------------------------------------------
# 3. Добавление ингредиентов
# ---------------------------------------------------------------
class TestAddIngredient:
    """Тесты метода add_ingredient."""

    def test_add_ingredient_appends_to_list(self, burger, mock_ingredient_sauce):
        # Действие: добавляем один ингредиент
        burger.add_ingredient(mock_ingredient_sauce)

        # Проверка: ингредиент оказался в списке
        assert burger.ingredients == [mock_ingredient_sauce]

    def test_add_ingredient_preserves_order(self, burger,
                                             mock_ingredient_sauce,
                                             mock_ingredient_filling):
        # Действие: добавляем два ингредиента по очереди
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Проверка: порядок в списке соответствует порядку добавления
        assert burger.ingredients == [mock_ingredient_sauce,
                                      mock_ingredient_filling]


# ---------------------------------------------------------------
# 4. Удаление ингредиентов
# ---------------------------------------------------------------
class TestRemoveIngredient:
    """Тесты метода remove_ingredient."""

    def test_remove_ingredient_by_index(self, burger,
                                        mock_ingredient_sauce,
                                        mock_ingredient_filling):
        # Подготовка: в списке два ингредиента
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Действие: удаляем первый элемент (индекс 0)
        burger.remove_ingredient(0)

        # Проверка: остался только второй ингредиент
        assert burger.ingredients == [mock_ingredient_filling]

    def test_remove_ingredient_from_empty_list_raises(self, burger):
        # Действие и проверка: удаление из пустого списка вызывает IndexError
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_remove_ingredient_invalid_index_raises(self, burger,
                                                    mock_ingredient_sauce):
        # Подготовка: один ингредиент (валидный индекс — только 0)
        burger.add_ingredient(mock_ingredient_sauce)

        # Действие и проверка: индекс 1 выходит за границы списка
        with pytest.raises(IndexError):
            burger.remove_ingredient(1)


# ---------------------------------------------------------------
# 5. Перемещение ингредиентов
# ---------------------------------------------------------------
class TestMoveIngredient:
    """Тесты метода move_ingredient."""

    def test_move_ingredient_forward(self, burger,
                                     mock_ingredient_sauce,
                                     mock_ingredient_filling):
        # Подготовка: [соевый, курица]
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Действие: перемещаем элемент с индекса 0 на индекс 1
        burger.move_ingredient(0, 1)

        # Проверка: порядок изменился на [курица, соевый]
        assert burger.ingredients == [mock_ingredient_filling,
                                      mock_ingredient_sauce]

    def test_move_ingredient_backward(self, burger,
                                      mock_ingredient_sauce,
                                      mock_ingredient_filling):
        # Подготовка: [соевый, курица]
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Действие: перемещаем последний элемент на позицию 0
        burger.move_ingredient(1, 0)

        # Проверка: элемент встал в начало списка
        assert burger.ingredients == [mock_ingredient_filling,
                                      mock_ingredient_sauce]

    def test_move_ingredient_to_same_index(self, burger,
                                           mock_ingredient_sauce,
                                           mock_ingredient_filling):
        # Подготовка: два ингредиента
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Действие: перемещаем элемент на ту же позицию (0 -> 0)
        burger.move_ingredient(0, 0)

        # Проверка: список не изменился
        assert burger.ingredients == [mock_ingredient_sauce,
                                      mock_ingredient_filling]

    def test_move_ingredient_invalid_index_raises(self, burger,
                                                  mock_ingredient_sauce):
        # Подготовка: один ингредиент
        burger.add_ingredient(mock_ingredient_sauce)

        # Действие и проверка: pop по несуществующему индексу даёт IndexError
        with pytest.raises(IndexError):
            burger.move_ingredient(5, 0)


# ---------------------------------------------------------------
# 6. Расчёт цены
# ---------------------------------------------------------------
class TestGetPrice:
    """
    Тесты метода get_price.

    Формула: цена = (цена булочки × 2) + сумма цен ингредиентов.
    Цены берём из моков: булочка 100.0, соус 50.0, начинка 75.0.
    """

    def test_price_is_bun_only(self, burger, mock_bun):
        # Подготовка: только булочка, без ингредиентов
        burger.set_buns(mock_bun)

        # Проверка: 100 × 2 = 200
        assert burger.get_price() == 200.0

    def test_price_with_one_ingredient(self, burger,
                                       mock_bun,
                                       mock_ingredient_sauce):
        # Подготовка: булочка + один соус
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)

        # Проверка: 100 × 2 + 50 = 250
        assert burger.get_price() == 250.0

    def test_price_with_multiple_ingredients(self, burger,
                                             mock_bun,
                                             mock_ingredient_sauce,
                                             mock_ingredient_filling):
        # Подготовка: булочка + соус + начинка
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Проверка: 100 × 2 + 50 + 75 = 325
        assert burger.get_price() == 325.0

    def test_get_price_calls_bun_get_price_once(self, burger, mock_bun):
        """
        Проверка взаимодействия: get_price должен вызвать
        get_price у булочки ровно один раз.
        """
        burger.set_buns(mock_bun)

        # Действие: считаем цену
        burger.get_price()

        # Проверка: мок-булочка отработала ровно 1 раз
        mock_bun.get_price.assert_called_once()

    def test_get_price_calls_each_ingredient_once(self, burger,
                                                  mock_bun,
                                                  mock_ingredient_filling):
        """Проверка взаимодействия: у каждого ингредиента get_price — 1 раз."""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_filling)

        burger.get_price()

        mock_ingredient_filling.get_price.assert_called_once()

    @pytest.mark.parametrize(
        'bun_price, ingredient_prices, expected',
        [
            # без ингредиентов
            (10.0, [], 20.0),
            # один ингредиент
            (50.5, [25.25], 126.25),
            # несколько одинаковых ингредиентов
            (30.0, [5.0, 5.0, 5.0], 75.0),
        ],
        ids=['только булочка', 'один ингредиент', 'три ингредиента'],
    )
    def test_price_calculation_parametrized(self, burger, bun_price,
                                            ingredient_prices, expected):
        """
        Параметризованная проверка формулы цены.
        Моки создаются локально с нужными ценами.
        """
        # Подготовка: булочка-мок с заданной ценой
        bun = Mock()
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)

        # Подготовка: ингредиенты-моки с заданными ценами
        for price in ingredient_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        # Проверка: фактическая цена совпадает с ожидаемой
        assert burger.get_price() == expected


# ---------------------------------------------------------------
# 7. Чек (get_receipt)
# ---------------------------------------------------------------
class TestGetReceipt:
    """
    Тесты метода get_receipt.

    Ожидаемый формат чека:
    (==== имя булочки ====)
    = <тип в нижнем регистре> <название ингредиента> =
    (==== имя булочки ====)
    <пустая строка>
    Price: <цена>
    """

    def test_receipt_with_single_ingredient(self, burger,
                                            mock_bun,
                                            mock_ingredient_sauce):
        # Подготовка: булочка + соус
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)

        # Действие: получаем чек
        receipt = burger.get_receipt()

        # Проверка: чек собран построчно в правильном формате
        expected = (
            '(==== белый хлеб ====)\n'
            '= sauce майонез =\n'
            '(==== белый хлеб ====)\n'
            '\n'
            'Price: 250.0'
        )
        assert receipt == expected

    def test_receipt_ingredient_type_is_lowercase(self, burger,
                                                  mock_bun,
                                                  mock_ingredient_filling):
        """
        Мок возвращает тип 'FILLING' (как в ingredient_types.INGREDIENT_TYPE_FILLING),
        а в чеке тип должен быть в нижнем регистре — 'filling'.
        """
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_filling)

        receipt = burger.get_receipt()

        # Проверка: строка с ингредиентом содержит 'filling', а не 'FILLING'
        assert '= filling курица =' in receipt

    def test_receipt_price_matches_get_price(self, burger,
                                             mock_bun,
                                             mock_ingredient_sauce):
        # Подготовка: булочка + соус
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)

        # Действие: получаем чек и цену независимо
        receipt = burger.get_receipt()
        actual_price = burger.get_price()

        # Проверка: цена в чеке совпадает с результатом get_price
        assert f'Price: {actual_price}' in receipt

    def test_receipt_bun_name_appears_twice(self, burger, mock_bun,
                                            mock_ingredient_filling):
        # Подготовка: булочка + начинка
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_filling)

        # Действие: получаем чек
        receipt = burger.get_receipt()

        # Проверка: название булочки встречается дважды (верх и низ чека)
        assert receipt.count('(==== белый хлеб ====)') == 2

    def test_receipt_is_string(self, burger, mock_bun):
        # Подготовка: только булочка
        burger.set_buns(mock_bun)

        # Проверка: get_receipt возвращает строку
        assert isinstance(burger.get_receipt(), str)

    def test_receipt_ingredients_order_follows_list(self, burger,
                                                    mock_bun,
                                                    mock_ingredient_sauce,
                                                    mock_ingredient_filling):
        # Подготовка: соус, затем начинка
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        # Действие: получаем чек
        receipt = burger.get_receipt()

        # Проверка: соус в чеке идёт раньше начинки
        assert receipt.index('= sauce майонез =') < \
            receipt.index('= filling курица =')
