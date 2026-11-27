"""
Юнит-тесты функции main() из praktikum.py.

Функция main() — сценарий сборки бургера:
  1. Создаёт базу данных и бургер.
  2. Берёт доступные булки и ингредиенты из базы.
  3. Кладёт первую булку, добавляет 4 ингредиента (по индексам 1, 4, 3, 5).
  4. Перемещает ингредиент с позиции 2 на позицию 1.
  5. Удаляет ингредиент с позиции 3.
  6. Печатает чек.

Тестирование построено двумя способами:
  - ISOLATED: классы Database и Burger подменяются моками через
    unittest.mock.patch — проверяем ТОЛЬКО логику сценария
    (какие методы и с какими аргументами вызывает main()).
    Мок-база берётся из фикстуры mock_database (conftest.py).
  - INTEGRATION: один тест на реальных объектах — проверяем,
    что сценарий выполняется целиком и печатает чек в stdout.

Важно: патчим praktikum.praktikum.Database (а не praktikum.database),
потому что main() импортирует классы в СВОЁ пространство имён —
подменять имя нужно там, где оно используется.
"""
from unittest.mock import patch, call

from praktikum.praktikum import main


# ---------------------------------------------------------------
# 1. Изолированные тесты: main() с моками Database и Burger
# ---------------------------------------------------------------
class TestMainIsolated:
    """Проверяем, что main() правильно управляет объектами."""

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_creates_database_and_burger(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: база данных создана ровно один раз, без аргументов
        mock_database_class.assert_called_once_with()

        # Проверка: бургер создан ровно один раз, без аргументов
        mock_burger_class.assert_called_once_with()

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_set_buns_uses_first_bun(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, buns, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: в бургер положена именно первая булка из базы
        mock_burger_class.return_value.set_buns.assert_called_once_with(buns[0])

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_gets_buns_and_ingredients_from_database(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: сценарий запросил из базы и булки, и ингредиенты,
        # каждый список — ровно один раз
        database.available_buns.assert_called_once_with()
        database.available_ingredients.assert_called_once_with()

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_adds_ingredients_in_expected_order(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, ingredients = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: добавлены ингредиенты с индексами 1, 4, 3, 5 —
        # ровно в этом порядке и без лишних вызовов
        expected = [
            call(ingredients[1]),
            call(ingredients[4]),
            call(ingredients[3]),
            call(ingredients[5]),
        ]
        assert mock_burger_class.return_value.add_ingredient.call_args_list == expected

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_moves_ingredient(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: перемещение вызвано один раз с аргументами (2, 1)
        mock_burger_class.return_value.move_ingredient.assert_called_once_with(2, 1)

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_removes_ingredient(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: удаление вызвано один раз с аргументом 3
        mock_burger_class.return_value.remove_ingredient.assert_called_once_with(3)

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_get_receipt_called_once(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий
        main()

        # Проверка: чек запрошен ровно один раз, без аргументов
        mock_burger_class.return_value.get_receipt.assert_called_once_with()


# ---------------------------------------------------------------
# 2. Тест вывода: чек печатается в stdout
# ---------------------------------------------------------------
class TestMainOutput:
    """Проверяем, что main() печатает чек."""

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_receipt_printed_to_stdout(self, mock_database_class, mock_burger_class, mock_database, capsys):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: задаём мок-бургеру фиксированный текст чека
        mock_burger_class.return_value.get_receipt.return_value = '(==== test ====)'

        # Шаг 3: запускаем сценарий
        main()

        # Шаг 4: читаем то, что попало в stdout через capsys
        captured = capsys.readouterr()

        # Проверка: в выводе есть текст чека
        assert '(==== test ====)' in captured.out

    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.Database')
    def test_main_returns_none(self, mock_database_class, mock_burger_class, mock_database):
        # Шаг 1: берём мок-базу из фикстуры и подменяем ею класс Database
        database, _, _ = mock_database
        mock_database_class.return_value = database

        # Шаг 2: запускаем сценарий и проверяем возвращаемое значение:
        # main() ничего не возвращает (None) — она только печатает чек
        assert main() is None


# ---------------------------------------------------------------
# 3. Интеграционный тест: main() на реальных объектах
# ---------------------------------------------------------------
class TestMainIntegration:
    """
    Сквозной тест: main() с настоящими Database и Burger (без моков).
    Проверяем, что сценарий выполняется без ошибок и печатает
    чек с реальными данными из базы.
    """

    def test_receipt_contains_real_database_data(self, capsys):
        # Шаг 1: запускаем сценарий целиком, без моков
        main()

        # Шаг 2: читаем вывод
        captured = capsys.readouterr()
        output = captured.out

        # Проверка 1: вывод не пустой
        assert len(output) > 0

        # Проверка 2: в чеке есть название булки
        # (в чеке она печатается дважды — верх и низ бургера)
        assert '(==== black bun ====)' in output

        # Проверка 3: состав ингредиентов после всех операций.
        # Добавляли индексы 1, 4, 3, 5 → список:
        #   [sour cream, dinosaur, cutlet, sausage]
        # move_ingredient(2, 1) → [sour cream, cutlet, dinosaur, sausage]
        # remove_ingredient(3) → удалили sausage, осталось:
        #   [sour cream, cutlet, dinosaur]
        for name in ('sour cream', 'cutlet', 'dinosaur'):
            assert name in output

        # Удалённый ингредиент в чеке появляться не должен
        assert 'sausage' not in output

        # Проверка 4: в чеке есть строка с ценой
        assert 'Price:' in output

