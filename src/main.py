"""CLI-приложение для визуализации графа зависимостей."""

import argparse
import sys

from src.fetcher import PackageFetcher


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

    args = parser.parse_args()

    if args.max_depth < 1:
        print("Ошибка: максимальная глубина должна быть больше 0", file=sys.stderr)
        sys.exit(1)

    return args


def main() -> None:
    """Точка входа в приложение."""
    args = parse_arguments()
    
    # Вывод параметров (оставляем для проверки)
    print("--- Параметры запуска ---")
    print(f"package: {args.package}")
    print(f"repo: {args.repo}")
    print(f"test_mode: {args.test_mode}")
    print(f"version: {args.version}")
    print(f"max_depth: {args.max_depth}")
    print(f"filter: {args.filter}")
    print("-------------------------\n")

    # Сбор данных (Этап 2)
    fetcher = PackageFetcher(args.repo, args.test_mode)
    
    print(f"Поиск прямых зависимостей для пакета '{args.package}'...")
    dependencies = fetcher.get_dependencies(args.package, args.version)
    
    if not dependencies:
        print("Прямых зависимостей не найдено (или произошла ошибка).")
    else:
        print("Прямые зависимости:")
        for dep in dependencies:
            print(f" - {dep}")


if __name__ == "__main__":
    main()
