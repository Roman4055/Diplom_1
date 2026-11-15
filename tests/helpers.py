from unittest.mock import Mock


def make_bun(name='белый хлеб', price=100.0):
    """
    Мок булочки.

    Аргументы:
      name  — то, что вернёт get_name();
      price — то, что вернёт get_price().

    Возвращает Mock с настроенными геттерами.
    """
    bun = Mock()
    bun.get_name.return_value = name
    bun.get_price.return_value = price
    return bun


def make_ingredient(ing_type='SAUCE', name='майонез', price=50.0):
    """
    Мок ингредиента.

    Аргументы:
      ing_type — то, что вернёт get_type() ('SAUCE' или 'FILLING');
      name     — то, что вернёт get_name();
      price    — то, что вернёт get_price().

    Возвращает Mock с настроенными геттерами.
    """
    ingredient = Mock()
    ingredient.get_type.return_value = ing_type
    ingredient.get_name.return_value = name
    ingredient.get_price.return_value = price
    return ingredient

