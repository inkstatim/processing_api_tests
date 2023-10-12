from datetime import datetime
import time


class Waiter:

    @staticmethod
    def wait_for(condition_func, timeout=40, step=5, ignore_exception=True, **kwargs):
        """
        Ожидает выполнения условия, заданного в функции `condition_func`, в течение заданного времени.

        Args:
            condition_func (callable): Функция, содержащая условие, которое нужно ожидать.
            timeout (int): Максимальное время ожидания в секундах.
            step (int): Интервал проверки условия в секундах.
            ignore_exception (bool): Флаг, указывающий, следует ли игнорировать исключения,
                                    возникающие при выполнении `condition_func` (по умолчанию True).
            **kwargs: Дополнительные аргументы, передаваемые в `condition_func`.

        Returns:
            bool: True, если условие было выполнено; False, если время ожидания истекло.

        Raises:
            Exception: Если `ignore_exception` равно False и во время выполнения `condition_func`
                       возникло исключение, то будет сгенерировано исключение с сообщением об ошибке.
        """
        start = datetime.utcnow()
        while (datetime.utcnow() - start).seconds < timeout:
            try:
                if condition_func(*kwargs.values()):
                    return True
            except (IndexError, KeyError, AttributeError, TypeError) as error:
                if ignore_exception:
                    pass
                else:
                    raise Exception(f"catch exception while condition function execute: {error}")
            time.sleep(step)
        return False

    @staticmethod
    def request_with_retry(session, url, method, max_retries=3, wait_time=5, **kwargs):
        retries = 0
        while retries < max_retries:
            response = session.request(method, url, **kwargs)
            if response.status_code != 412:
                return response
            retries += 1
            time.sleep(wait_time)
        return response
