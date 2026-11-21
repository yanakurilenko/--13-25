"""Модуль для визуализации графа зависимостей (Вариант 13)."""

import argparse
import sys
import urllib.request
import os
import tempfile
import tarfile
import io


def download_deb(url: str) -> str | None:
    """Скачивает .deb файл по URL и возвращает путь к нему."""
    try:
        print(f"Скачивание пакета: {url}")
        fd, temp_path = tempfile.mkstemp(suffix=".deb")
        os.close(fd)
        urllib.request.urlretrieve(url, temp_path)
        return temp_path
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")
        return None


def parse_control_tar(data: bytes) -> list[str]:
    """Вспомогательная функция для парсинга control.tar."""
    depends_list = []
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tar:
        for member in tar.getmembers():
            if member.name in ("./control", "control"):
                file_obj = tar.extractfile(member)
                content = file_obj.read().decode('utf-8', errors='ignore')
                for line in content.split('\n'):
                    if line.startswith("Depends:"):
                        deps_str = line.replace("Depends:", "").strip()
                        return [
                            d.split('(')[0].strip()
                            for d in deps_str.split(',')
                        ]
    return depends_list


def extract_deb_native(deb_path: str) -> list[str]:
    """Извлекает зависимости из .deb файла без сторонних утилит."""
    try:
        with open(deb_path, "rb") as f:
            if f.read(8) != b"!<arch>\n":
                return []
            while True:
                header = f.read(60)
                if not header:
                    break
                filename = header[:16].decode('utf-8',
                                              errors='ignore').strip()
                size = int(header[48:58].decode(
                    'utf-8', errors='ignore').strip())

                if filename.startswith("control.tar"):
                    data = f.read(size)
                    return parse_control_tar(data)
                else:
                    f.seek(size, 1)
                if size % 2 != 0:
                    f.seek(1, 1)
    except Exception as e:
        print(f"Ошибка при извлечении: {e}")
    return []


def read_test_repo(filepath: str) -> dict[str, list[str]] | None:
    """Читает файл с тестовым графом зависимостей."""
    graph = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    pkg, deps = line.split(':', 1)
                    pkg = pkg.strip()
                    deps_list = [
                        d.strip() for d in deps.split(',') if d.strip()
                    ]
                    graph[pkg] = deps_list
        return graph
    except Exception as e:
        print(f"Ошибка чтения тестового файла: {e}")
        return None


def dfs_recursive(
    graph: dict[str, list[str]],
    node: str,
    visited: set[str],
    depth: int,
    max_depth: int | None,
    indent: str = ""
) -> None:
    """Алгоритм DFS с рекурсией для обхода графа зависимостей."""
    if max_depth is not None and depth > max_depth:
        print(f"{indent}└── {node} (обрезано: превышена глубина)")
        return

    if node in visited:
        print(f"{indent}└── {node} (циклическая зависимость)")
        return

    print(f"{indent}├── {node}")
    visited.add(node)

    if node in graph:
        for child in graph[node]:
            dfs_recursive(
                graph, child, visited, depth + 1,
                max_depth, indent + "│   "
            )


def run_test_mode(args: argparse.Namespace) -> None:
    """Запускает логику тестового режима."""
    print(f"Запуск в тестовом режиме. Чтение графа из {args.repo_url}...")
    graph = read_test_repo(args.repo_url)
    if graph is None:
        sys.exit(1)

    if args.package not in graph:
        print(f"Ошибка: Пакет '{args.package}' не найден.")
        sys.exit(1)

    print(f"\nГраф зависимостей для {args.package}:")
    visited_nodes = set()
    dfs_recursive(graph, args.package, visited_nodes, 0, args.max_depth)


def run_real_mode(args: argparse.Namespace) -> None:
    """Запускает логику скачивания и парсинга реального .deb файла."""
    print(f"Анализ пакета {args.package} версии {args.version}...")
    deb_path = download_deb(args.repo_url)
    if not deb_path:
        sys.exit(1)

    deps = extract_deb_native(deb_path)
    print(f"\nПрямые зависимости для {args.package}:")
    if deps:
        for dep in deps:
            print(f" - {dep}")
    else:
        print("Зависимости не найдены.")

    if os.path.exists(deb_path):
        os.remove(deb_path)


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Dependency Graph Visualizer (Variant 13)"
    )
    parser.add_argument(
        "--package", type=str, required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo-url", type=str, required=True,
        help="URL-адрес репозитория или путь к тестовому файлу"
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Режим тестового репозитория"
    )
    parser.add_argument(
        "--version", type=str, required=True, help="Версия пакета"
    )
    parser.add_argument(
        "--ascii-tree", action="store_true",
        help="Вывод в виде ASCII-дерева"
    )
    parser.add_argument(
        "--max-depth", type=int, default=None,
        help="Максимальная глубина анализа"
    )
    return parser.parse_args()


def main() -> None:
    """Главная функция приложения."""
    args = parse_arguments()

    print("--- Параметры запуска ---")
    print(f"Имя пакета: {args.package}")
    print(f"URL/Путь: {args.repo_url}")
    print(f"Режим тестирования: {'Да' if args.test_mode else 'Нет'}")
    print(f"Версия: {args.version}")
    print(f"ASCII-дерево: {'Да' if args.ascii_tree else 'Нет'}")
    print(f"Макс. глубина: {args.max_depth}")
    print("-------------------------\n")

    if args.test_mode:
        run_test_mode(args)
    else:
        run_real_mode(args)


if __name__ == "__main__":
    main()