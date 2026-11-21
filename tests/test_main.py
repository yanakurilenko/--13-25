"""Тесты для модуля main."""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), 
    '..')))

from src.main import validate_arguments


class MockArgs:
    """Заглушка для аргументов."""
    def __init__(self, package, repo, test_mode):
        self.package = package
        self.repo = repo
        self.test_mode = test_mode


class TestConfigValidation(unittest.TestCase):
    """Тесты валидации конфигурации."""

    def test_empty_package_name(self):
        """Проверка ошибки при пустом имени 
        пакета."""
        args = MockArgs("", "http://test.com", 
            False)
        with self.assertRaises(ValueError) as ctx:
            validate_arguments(args)
        self.assertIn("Имя пакета не может "
            "быть пустым", str(ctx.exception))

    def test_empty_repo(self):
        """Проверка ошибки при пустом URL."""
        args = MockArgs("nginx", "", False)
        with self.assertRaises(ValueError) as ctx:
            validate_arguments(args)
        self.assertIn("Путь или URL репозитория "
            "не может быть пустым", 
            str(ctx.exception))


if __name__ == "__main__":
    unittest.main()