# release-tool - Tool to create project releases
#
# Copyright (C) 2019-2026  offa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re


class CMakeProject:
    __PATTERN = r"project\s*\((.+?)\)"
    PROJECT_CONFIG = "CMakeLists.txt"

    def __init__(self, proj_dir: str) -> None:
        self.__proj_dir = proj_dir
        project_args = self.__parse_project_arguments(
            _load_file(self.__proj_dir, self.PROJECT_CONFIG)
        )
        self.__name = project_args[0].strip()
        self.__version = project_args[_index_of(project_args, "VERSION") + 1].strip()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    @property
    def config_file(self) -> str:
        return os.path.abspath(os.path.join(self.__proj_dir, self.PROJECT_CONFIG))

    def set_new_version(self, new_version: str) -> None:
        content = _load_file(self.__proj_dir, self.PROJECT_CONFIG)
        match = re.search(self.__PATTERN, content, re.DOTALL)
        if match is None:
            raise ValueError(f"Invalid project(...): '{content}'")

        project_args = match.group(1).split(" ")
        idx = _index_of_version_value(project_args)
        project_args[idx] = _replace_version_value(project_args[idx], new_version)
        self.__version = new_version

        result = (
            content[: match.start(1)] + " ".join(project_args) + content[match.end(1) :]
        )
        _write_file(self.__proj_dir, self.PROJECT_CONFIG, result)

    def __parse_project_arguments(self, input_string: str) -> list[str]:
        match = re.search(self.__PATTERN, input_string, re.DOTALL)
        if not match:
            raise ValueError(f"Invalid project(...): '{input_string}'")
        args = match.group(1).split(" ")
        return [token for token in args if token.strip()]


def _index_of(args, name: str):
    for element in args:
        if element.strip() == name:
            return args.index(element)
    raise ValueError(f"No element '{name}' found in '{args}'")


def _index_of_version_value(args: list[str]) -> int:
    idx = _index_of(args, "VERSION") + 1
    while idx < len(args) and args[idx].strip() == "":
        idx += 1
    if idx >= len(args):
        raise ValueError("No version value found after 'VERSION' keyword")
    if args[idx].strip().startswith("#"):
        raise ValueError("Expected version value after 'VERSION' keyword")
    return idx


def _replace_version_value(token: str, new_version: str) -> str:
    return re.sub(
        r"^(\s*)\S+", lambda _match: _match.group(1) + new_version, token, count=1
    )


def _load_file(path: str, filename: str) -> str:
    with open(os.path.join(path, filename), "r", encoding="utf-8") as file:
        return file.read()


def _write_file(path: str, filename: str, content: str) -> None:
    with open(os.path.join(path, filename), "w", encoding="utf-8") as file:
        file.write(content)
