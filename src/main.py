"""CLI-приложение для визуализации графа зависимостей."""

import argparse
import sys

from src.fetcher import PackageFetcher
from src.graph import DependencyGraph


def parse_arguments() -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (pip)"
    )
    
    parser.add_argument(
        "--package", 
        type=str, 
        required=True, 
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo", 
        type=str, 
        default="https://pypi.org/pypi", 
        help="URL-адрес репозитория или путь к тестовому файлу"
    )
    parser.add_argument(
        "--test-mode", 
        action="store_true", 
        help="Режим работы с тестовым локальным репозиторием"
    )
    parser.add_argument(
        "--version", 
        type=str, 
        default="latest", 
        help="Версия пакета"
    )
    parser.add_argument(
        "--max-depth", 
        type=int, 
        default=3, 
        help="Максимальная глубина анализа зависимостей"
    )
    parser.add_argument(
        "--filter", 
        type=str, 
        default="", 
        help="Подстрока для фильтрации пакетов"
    )
    parser.add_argument(
        "--reverse", 
        action="store_true", 
        help="Режим вывода обратных зависимостей"
    )
    parser.add_argument(
        "--target", 
        type=str, 
        default="", 
        help="Пакет, для которого ищем обратные зависимости"
    )

    args = parser.parse_args()

    if args.max_depth < 1:
        print("Ошибка: максимальная глубина должна быть больше 0", file=sys.stderr)
        sys.exit(1)

    return args


def main() -> None:
    """Точка входа в приложение."""
    args = parse_arguments()
    
    # Вывод параметров
    print("--- Параметры запуска ---")
    print(f"package: {args.package}")
    print(f"repo: {args.repo}")
    print(f"test_mode: {args.test_mode}")
    print(f"version: {args.version}")
    print(f"max_depth: {args.max_depth}")
    print(f"filter: {args.filter}")
    print(f"reverse: {args.reverse}")
    print(f"target: {args.target}")
    print("-------------------------\n")

    # Этап 3: Построение графа
    fetcher = PackageFetcher(args.repo, args.test_mode)
    graph = DependencyGraph(fetcher)
    
    print(f"Построение графа зависимостей для '{args.package}'...")
    graph.build_dfs(args.package, args.version, args.max_depth, args.filter)
    
    print("\n--- Граф зависимостей ---")
    graph.print_graph()

    # Этап 4: Обратные зависимости (если запрошено)
    if args.reverse:
        print("\n--- Обратные зависимости ---")
        target_pkg = args.target if args.target else args.package
        graph.print_reverse_dependencies(target_pkg)


if __name__ == "__main__":
    main()
