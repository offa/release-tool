# release-tool - Tool to create project releases
#
# Copyright (C) 2019  offa
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
    __PATTERN = 'project\\((.+?) VERSION (.+?)\\)'

    def __init__(self, proj_dir):
        self.__proj_dir = proj_dir
        self.__version = None
        self.__name = None


    def path(self):
        return self.__proj_dir


    def name(self):
        return self.__name


    def version(self):
        return self.__version


    def project_config(self):
        return 'CMakeLists.txt'


    def set_version(self, new_version):
        self.__version = new_version


    def load(self):
        content = self._load_file(self.__proj_dir, self.project_config())
        m = re.search(self.__PATTERN, content)

        self.__name = (m.group(1))
        self.set_version(m.group(2))


    def store(self):
        content = self._load_file(self.__proj_dir, self.project_config())
        updated = r'project(\1 VERSION {})'.format(self.version())
        result = re.sub(self.__PATTERN, updated, content)

        self._store_file(self.__proj_dir, self.project_config(), result)


    def _load_file(self, path, file):
        with open(os.path.join(path, file)) as f:
            return f.read()
        return None


    def _store_file(self, path, file, content):
        with open(os.path.join(path, file), 'w') as f:
            f.write(content)
