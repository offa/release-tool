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
        self.version = None
        self.__name = None

    def path(self):
        return self.__proj_dir

    def name(self):
        return self.__name

    def load(self):
        content = _load_file(self.__proj_dir, self.PROJECT_CONFIG)
        self.__name, self.version = self.parse_project_config(content)

    def parse_project_config(self, input_string):
        project_args = self.__parse_project_arguments(input_string)
        name = project_args[0]
        version = project_args[project_args.index("VERSION") + 1]

        return (name, version)

    def store(self):
        content = _load_file(self.__proj_dir, self.PROJECT_CONFIG)
        project_args = self.__parse_project_arguments(content)
        project_args[project_args.index("VERSION") + 1] = self.version
        result = re.sub(self.__PATTERN, "project({})".format(" ".join(project_args)), content)

        _store_file(self.__proj_dir, self.PROJECT_CONFIG, result)

    def __parse_project_arguments(self, input_string):
        match = re.search(self.__PATTERN, input_string, re.DOTALL)
        return match.group(1).split()



def _load_file(path, filename):
    with open(os.path.join(path, filename)) as file:
        return file.read()
    return None


def _store_file(path, filename, content):
    with open(os.path.join(path, filename), 'w') as file:
        file.write(content)
