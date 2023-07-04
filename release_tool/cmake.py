# release-tool - Tool to create project releases
#
# Copyright (C) 2019-2023  offa
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


class CMakeProject():
    __PATTERN = r'project\s*\((.+?)\)'
    PROJECT_CONFIG = "CMakeLists.txt"

    def __init__(self, proj_dir):
        self.__proj_dir = proj_dir
        project_args = self.__parse_project_arguments(
            _load_file(self.__proj_dir, self.PROJECT_CONFIG))
        self.__name = project_args[0].strip()
        self.__version = project_args[_index_of(project_args, "VERSION") + 1].strip()

    @property
    def path(self):
        return self.__proj_dir

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    def set_new_version(self, new_version):
        content = _load_file(self.__proj_dir, self.PROJECT_CONFIG)
        project_args = self.__parse_project_arguments(content, True)
        self.__version = new_version

        idx = _index_of(project_args, "VERSION") + 1
        suffix = "\n" if project_args[idx].endswith(("\n", "\r")) else ""
        project_args[idx] = self.__version + suffix

        result = re.sub(self.__PATTERN,
                        f"project({' '.join(project_args)})",
                        content,
                        flags=re.DOTALL)
        _write_file(self.__proj_dir, self.PROJECT_CONFIG, result)

    def __parse_project_arguments(self, input_string, keep_whitespaces=False):
        match = re.search(self.__PATTERN, input_string, re.DOTALL)
        args = match.group(1).split(" ")
        return args if keep_whitespaces else [token for token in args if token.strip()]


def _index_of(args, name):
    for element in args:
        if element.strip() == name:
            return args.index(element)
    raise ValueError(f"No element '{name}' found in '{args}'")


def _load_file(path, filename):
    with open(os.path.join(path, filename), 'r', encoding="utf-8") as file:
        return file.read()


def _write_file(path, filename, content):
    with open(os.path.join(path, filename), 'w', encoding="utf-8") as file:
        file.write(content)
