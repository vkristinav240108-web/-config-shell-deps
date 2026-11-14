"""Модуль построения графа зависимостей."""

from typing import Dict, List, Set
from src.fetcher import PackageFetcher


class DependencyGraph:
    """Класс для построения и хранения графа зависимостей."""

    def __init__(self, fetcher: PackageFetcher) -> None:
        """Инициализация с объектом загрузчика."""
        self.fetcher = fetcher
        self.graph: Dict[str, List[str]] = {}

    def build_dfs(
        self, 
        start_package: str, 
        version: str, 
        max_depth: int, 
        filter_str: str
    ) -> None:
        """Строит граф зависимостей с помощью DFS без рекурсии.
        
        Использует стек для обхода. Обрабатывает циклы и глубину.
        """
        # Стек хранит кортежи: (имя_пакета, текущая_глубина)
        stack: List[tuple[str, int]] = [(start_package, 0)]
        # Множество посещенных пакетов для предотвращения циклов
        visited: Set[str] = set()

        while stack:
            current_pkg, current_depth = stack.pop()

            # Проверка на цикл или уже обработанный пакет
            if current_pkg in visited:
                continue
            
            # Проверка глубины
            if current_depth > max_depth:
                continue

            # Проверка фильтра (если подстрока есть в имени — пропускаем)
            if filter_str and filter_str in current_pkg:
                continue

            visited.add(current_pkg)
            
            # Получаем прямые зависимости для текущего пакета
            deps = self.fetcher.get_dependencies(current_pkg, version)
            
            # Сохраняем в граф
            self.graph[current_pkg] = deps

            # Добавляем зависимости в стек для дальнейшего обхода
            # Идем в обратном порядке, чтобы сохранить порядок вывода (опционально)
            for dep in reversed(deps):
                if dep not in visited:
                    stack.append((dep, current_depth + 1))

    def print_graph(self) -> None:
        """Выводит граф в консоль."""
        for pkg, deps in self.graph.items():
            deps_str = ", ".join(deps) if deps else "нет"
            print(f"{pkg} -> {deps_str}")
    def print_reverse_dependencies(self, target_package: str) -> None:
        """Выводит пакеты, которые зависят от заданного (обратные связи)."""
        reverse_deps = []
        
        # Проходим по всему графу
        for pkg, deps in self.graph.items():
            if target_package in deps:
                reverse_deps.append(pkg)
                
        if reverse_deps:
            print(f"Пакеты, которые зависят от '{target_package}':")
            for pkg in reverse_deps:
                print(f" - {pkg}")
        else:
            print(f"Пакетов, зависящих от '{target_package}', не найдено.")
