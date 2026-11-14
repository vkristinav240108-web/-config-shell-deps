"""Модуль получения данных о зависимостях пакетов pip."""

import json
import urllib.request
import urllib.error
from typing import Dict, List


class PackageFetcher:
    """Класс для загрузки зависимостей из репозитория или файла."""

    def __init__(self, repo_url: str, test_mode: bool = False) -> None:
        """Инициализация с URL репозитория и флагом тестового режима."""
        self.repo_url = repo_url
        self.test_mode = test_mode
        self._test_data = {}

        if self.test_mode:
            self._load_test_data()

    def _load_test_data(self) -> None:
        """Загружает тестовый JSON-файл."""
        try:
            with open(self.repo_url, "r", encoding="utf-8") as f:
                self._test_data = json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: тестовый файл '{self.repo_url}' не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка: неверный формат JSON в '{self.repo_url}'.")

    def get_dependencies(self, package_name: str, version: str) -> List[str]:
        """Возвращает список прямых зависимостей пакета."""
        if self.test_mode:
            return self._get_test_dependencies(package_name)
        else:
            return self._get_real_dependencies(package_name, version)

    def _get_test_dependencies(self, package_name: str) -> List[str]:
        """Получает зависимости из тестового словаря."""
        if package_name in self._test_data:
            return self._test_data[package_name].get("dependencies", [])
        return []

    def _get_real_dependencies(self, package_name: str, version: str) -> List[str]:
        """Получает зависимости из реального API PyPI."""
        url = f"{self.repo_url}/{package_name}/json"
        if version and version != "latest":
            url = f"{self.repo_url}/{package_name}/{version}/json"

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                requires = data.get("info", {}).get("requires_dist", [])
                if not requires:
                    return []
                
                deps = []
                for req in requires:
                    # Берем только имя пакета, отбрасывая версии и условия
                    dep_name = req.split(" ")[0]
                    for char in ["<", ">", "=", "!", "~", ";", "(", ")"]:
                        dep_name = dep_name.split(char)[0]
                    dep_name = dep_name.strip()
                    
                    if dep_name:
                        deps.append(dep_name)
                return deps
        except urllib.error.HTTPError:
            print(f"Ошибка: пакет '{package_name}' версии '{version}' не найден в PyPI.")
            return []
        except urllib.error.URLError:
            print("Ошибка: не удалось подключиться к репозиторию. Проверьте интернет.")
            return []
