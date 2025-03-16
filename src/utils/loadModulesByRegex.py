import os
import re
import importlib


def load_modules_by_regex(directory, pattern):
    """
    Загружает модули по регулярному выражению, рекурсивно проходя все подкаталоги.

    :param directory: Путь к директории, где ищем модули.
    :param pattern: Регулярное выражение для поиска файлов.
    """
    regex = re.compile(pattern)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if (
                filename.endswith(".py")
                and filename != "__init__.py"
                and regex.match(filename)
            ):
                print(filename)
                module_name = os.path.splitext(filename)[0]
                module_path = os.path.relpath(root, directory).replace(
                    os.sep, "."
                )

                if module_path == ".":
                    module_path = module_name

                full_module_path = f"{module_path}.{module_name}"

                try:
                    print(f"Импортируем модуль: {full_module_path}")
                    importlib.import_module(full_module_path)
                except ImportError as e:
                    print(f"Ошибка при импорте модуля {full_module_path}: {e}")
