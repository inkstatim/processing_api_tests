from typing import Callable

from utils.waiter import Waiter


class CommonCheckers:

    @staticmethod
    def assert_val(response: Callable, actual_path: str, expected_val: str):
        """
        Проверяет, что значение по указанному пути в словаре `response` соответствует ожидаемому значению.

        Args:
            response (Callable): Функция возвращающая словарь данных для проверки.
            actual_path (str): Путь к значению, разделенный точками.
            expected_val: Ожидаемое значение.

        Raises:
            AssertionError: Если фактическое значение не совпадает с ожидаемым.
        """
        # toDo вынести waiter от ассерта
        # toDo не делать новый запрос для нового поля, если оно уже в нужном состоянии
        assert Waiter.wait_for(lambda: CommonCheckers._get_val_by_path(response(), actual_path) == expected_val), \
            "expected '{}', but actual '{}' in '{}'".format(
                expected_val,
                CommonCheckers._get_val_by_path(
                    response(),
                    actual_path
                ),
                actual_path)

    @staticmethod
    def assert_all(response: dict, actual_path: str, expected_val: str):
        """
        Проверяет, что все значения по указанному пути в данных соответствуют ожидаемому значению.

        Args:
            response (dict): Словарь данных для проверки.
            actual_path (str): Путь к значению, разделенный точками.
            expected_val: Ожидаемое значение.

        Raises:
            AssertionError: Если хотя бы одно фактическое значение не совпадает с ожидаемым.
        """
        actual_data = CommonCheckers._get_all_by_path(response, actual_path)
        for item in actual_data:
            assert item == expected_val, \
                f"expected '{expected_val}', but actual '{item}' for all entities at path '{actual_path}' different"

    @staticmethod
    def _get_val_by_path(data: dict, actual_path: str) -> dict:
        """
        Получает значение из словаря данных по указанному пути.

        Args:
            data (dict): Словарь, из которого извлекается значение.
            actual_path (str): Путь к значению, разделенный точками.

        Returns:
            dict: Значение, извлеченное из данных по указанному пути.
        """
        if '.' not in actual_path:
            return data[actual_path]
        keys = actual_path.split('.')
        for key in keys:
            if type(data) is not dict:
                raise TypeError(f"expected type of 'response' is dict, actual type: {type(data)}")
            data = data.get(key, {})
        return data

    @staticmethod
    def _get_all_by_path(data: dict, actual_path: str) -> dict:
        """
        Получает значение из списка данных по указанному пути.

        Args:
            data (dict): Список, из которого извлекается значение.
            actual_path (str): Путь к значению, разделенный точками.

        Returns:
            dict: Значение, извлеченное из данных по указанному пути.
        """
        keys = actual_path.split('.')
        for key in keys:
            if isinstance(data, list):
                data = [item.get(key, {}) for item in data]
            else:
                data = data.get(key, {})
        return data
