
from time import time


class UserModelUtils():
    """
        Утилиты для кастомной модели Пользователя
    """

    @classmethod
    def get(cls) -> str:
        """
            Получение стандартного имени Пользователя
        """

        return f'Username_{int(time() * 1000)}'
