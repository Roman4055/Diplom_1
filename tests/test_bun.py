"""Юнит-тесты класса Bun — здесь используются реальные объекты."""
from praktikum.bun import Bun


class TestBun:

    def test_get_name_returns_name(self):
        # Подготовка: булочка с названием и ценой
        bun = Bun('чёрный булка', 42.0)

        # Проверка: get_name вернёт то, что передали в конструктор
        assert bun.get_name() == 'чёрный булка'

    def test_get_price_returns_price(self):
        bun = Bun('чёрный булка', 42.0)

        assert bun.get_price() == 42.0
