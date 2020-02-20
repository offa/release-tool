# release-tool - Tool to create project releases
#
# Copyright (C) 2019-2020  offa
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
        self.__name = project_args[0]
        self.__version = project_args[project_args.index("VERSION") + 1]

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
        project_args = self.__parse_project_arguments(content)
        self.__version = new_version
        project_args[project_args.index("VERSION") + 1] = self.__version
        result = re.sub(self.__PATTERN, "project({})".format(" ".join(project_args)), content)
        _write_file(self.__proj_dir, self.PROJECT_CONFIG, result)

    def __parse_project_arguments(self, input_string):
        match = re.search(self.__PATTERN, input_string, re.DOTALL)
        return match.group(1).split()


def _load_file(path, filename):
    with open(os.path.join(path, filename)) as file:
        return file.read()
    return None


def _write_file(path, filename, content):
    with open(os.path.join(path, filename), 'w') as file:
        file.write(content)
