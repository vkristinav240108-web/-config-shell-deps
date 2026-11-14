"""Модуль визуализации графа в формате D2."""

from typing import Dict, List


class GraphVisualizer:
    """Класс для генерации описания графа на языке D2."""

    def __init__(self, graph_data: Dict[str, List[str]]) -> None:
        """Инициализация с данными графа."""
        self.graph_data = graph_data

    def generate_d2(self) -> str:
        """Генерирует текстовое описание графа на языке D2."""
        lines = ["direction: right"]
        
        for pkg, deps in self.graph_data.items():
            if not deps:
                lines.append(f'"{pkg}"')
            else:
                for dep in deps:
                    lines.append(f'"{pkg}" -> "{dep}"')
                    
        return "\n".join(lines)
