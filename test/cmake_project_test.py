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

import unittest
from unittest.mock import patch
from release_tool.cmake import CMakeProject

CMAKE_CONTENT = 'cmake_minimum_required(VERSION 3.14)\n\n' \
    'project(TestProj VERSION {})\n\n'


class TestCMakeProject(unittest.TestCase):

    def test_default_values(self):
        proj = CMakeProject('x')
        self.assertEqual(proj.name(), None)
        self.assertEqual(proj.version, None)
        self.assertEqual(proj.path(), 'x')
        self.assertEqual(proj.project_config(), 'CMakeLists.txt')

    def test_parse_project_config_parses_values(self):
        proj = CMakeProject('abc')
        name, version = proj.parse_project_config(CMAKE_CONTENT.format('1.23.456'))

        self.assertEqual(name, 'TestProj')
        self.assertEqual(version, '1.23.456')

    def test_parse_project_config_handles_whitespaces(self):
        content_ws = 'cmake_minimum_required(VERSION 3.14)\n\n' \
            '  \n \t project  (\n\n\t TestProj \n  \nVERSION \n {} \n)\n\n'
        proj = CMakeProject('abc')
        name, version = proj.parse_project_config(content_ws.format('395.18.20'))

        self.assertEqual(name, 'TestProj')
        self.assertEqual(version, '395.18.20')

    def test_parse_project_config_handles_additional_arguments(self):
        content_ws = 'cmake_minimum_required(VERSION 3.14)\n\n' \
            'project(TestProj DESCRIPTION "text" VERSION {} LANGUAGES CXX C)'
        proj = CMakeProject('abc')
        name, version = proj.parse_project_config(content_ws.format('395.18.20'))

        self.assertEqual(name, 'TestProj')
        self.assertEqual(version, '395.18.20')

    @patch('release_tool.cmake._load_file', return_value=CMAKE_CONTENT.format('1.41.5'))
    def test_load_reads_data(self, mock_load_file):
        proj = CMakeProject('x/proj-a')

        proj.load()

        self.assertEqual(proj.version, '1.41.5')
        self.assertEqual(proj.name(), 'TestProj')

        mock_load_file.assert_called_with(proj.path(), 'CMakeLists.txt')

    @patch('release_tool.cmake._store_file')
    @patch('release_tool.cmake._load_file', return_value=CMAKE_CONTENT.format('0.0.1'))
    def test_store_writes_data(self, _mock_load_file, mock_store_file):
        proj = _mock_load()
        proj.version = '1.9.10'
        proj.store()

        self.assertEqual(proj.version, '1.9.10')
        mock_store_file.assert_called_with(proj.path(), 'CMakeLists.txt',
                                           CMAKE_CONTENT.format('1.9.10'))

    @patch('release_tool.cmake._store_file')
    def test_store_keeps_existing_values(self, mock_store_file):
        proj = _mock_load()
        proj.version = '4.8.2'

        cmake_content_extended = 'cmake_minimum_required(VERSION 3.14)\n' \
            'project(TestProj LANGUAGES CXX VERSION {} DESCRIPTION "Additional values here")'

        with patch('release_tool.cmake._load_file',
                   return_value=cmake_content_extended.format('0.1.2')):
            proj.store()

        self.assertEqual(proj.version, '4.8.2')
        mock_store_file.assert_called_with(proj.path(), 'CMakeLists.txt',
                                           cmake_content_extended.format('4.8.2'))

    def test_current_version(self):
        proj = _mock_load()

        self.assertEqual(proj.version, '0.1.2')

    def test_set_new_version(self):
        proj = _mock_load()

        self.assertEqual(proj.version, '0.1.2')
        proj.version = '1.3.4'
        self.assertEqual(proj.version, '1.3.4')


def _mock_load():
    with patch('release_tool.cmake._load_file', return_value=CMAKE_CONTENT.format('0.1.2')):
        proj = CMakeProject('x')
        proj.load()

        return proj


if __name__ == '__main__':
    unittest.main()
