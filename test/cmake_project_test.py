# release-tool - Tool to create project releases
#
# Copyright (C) 2019-2025  offa
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

CMAKE_CONTENT = (
    "cmake_minimum_required(VERSION 3.14)\n\nproject(TestProj VERSION {})\n\n"
)


class TestCMakeProject(unittest.TestCase):
    @patch(
        "release_tool.cmake._load_file", return_value=CMAKE_CONTENT.format("1.23.456")
    )
    def test_parse_project_config_parses_values(self, _mock_load_file):
        proj = CMakeProject("abc")

        self.assertEqual(proj.name, "TestProj")
        self.assertEqual(proj.version, "1.23.456")

    @patch(
        "release_tool.cmake._load_file",
        return_value="""
cmake_minimum_required(VERSION 3.15)

project(project-name-1
  VERSION 1.16.7
  DESCRIPTION "An example project"
  LANGUAGES CXX
)
""",
    )
    def test_parse_project_config_parses_values_multiline(self, _mock_load_file):
        proj = CMakeProject("abc")

        self.assertEqual(proj.name, "project-name-1")
        self.assertEqual(proj.version, "1.16.7")

    def test_parse_project_config_handles_whitespaces(self):
        content_ws = (
            "cmake_minimum_required(VERSION 3.14)\n\n"
            "  \n \t project  (\n\n\t TestProj \n  \nVERSION \n {} \n)\n\n"
        )

        with patch(
            "release_tool.cmake._load_file", return_value=content_ws.format("395.18.20")
        ):
            proj = CMakeProject("abc")

        self.assertEqual(proj.name, "TestProj")
        self.assertEqual(proj.version, "395.18.20")

    def test_parse_project_config_handles_additional_arguments(self):
        content_ws = (
            "cmake_minimum_required(VERSION 3.14)\n\n"
            'project(TestProj DESCRIPTION "text" VERSION {} LANGUAGES CXX C)'
        )

        with patch(
            "release_tool.cmake._load_file", return_value=content_ws.format("1.18.203")
        ):
            proj = CMakeProject("abc")

        self.assertEqual(proj.name, "TestProj")
        self.assertEqual(proj.version, "1.18.203")

    @patch("release_tool.cmake._load_file", return_value=CMAKE_CONTENT.format("1.41.5"))
    def test_load_reads_data(self, mock_load_file):
        proj = CMakeProject("x/proj-a")

        self.assertEqual(proj.version, "1.41.5")
        self.assertEqual(proj.name, "TestProj")

        mock_load_file.assert_called_with("x/proj-a", "CMakeLists.txt")

    @patch("release_tool.cmake._write_file")
    @patch("release_tool.cmake._load_file", return_value=CMAKE_CONTENT.format("0.0.1"))
    def test_set_new_version_writes_data(self, _mock_load_file, mock_write_file):
        proj = _mock_load()
        proj.set_new_version("1.9.10")

        self.assertEqual(proj.version, "1.9.10")
        mock_write_file.assert_called_with(
            "x", "CMakeLists.txt", CMAKE_CONTENT.format("1.9.10")
        )

    @patch("release_tool.cmake._write_file")
    def test_set_new_version_keeps_formatting(self, mock_write_file):
        proj = _mock_load()

        cmake_content_extended = """
cmake_minimum_required(VERSION 3.15)

project(project-name-1
  VERSION {}
  DESCRIPTION "An example project"
  LANGUAGES CXX
)
"""
        with patch(
            "release_tool.cmake._load_file",
            return_value=cmake_content_extended.format("0.1.2"),
        ):
            proj.set_new_version("4.8.2")

        self.assertEqual(proj.version, "4.8.2")
        mock_write_file.assert_called_with(
            "x", "CMakeLists.txt", cmake_content_extended.format("4.8.2")
        )

    @patch("release_tool.cmake._write_file")
    def test_set_new_version_keeps_existing_values(self, mock_write_file):
        proj = _mock_load()

        cmake_content_extended = (
            "cmake_minimum_required(VERSION 3.14)\n"
            'project(TestProj LANGUAGES CXX VERSION {} DESCRIPTION "Additional values here")'
        )

        with patch(
            "release_tool.cmake._load_file",
            return_value=cmake_content_extended.format("0.1.2"),
        ):
            proj.set_new_version("4.8.2")

        self.assertEqual(proj.version, "4.8.2")
        mock_write_file.assert_called_with(
            "x", "CMakeLists.txt", cmake_content_extended.format("4.8.2")
        )

    @patch("release_tool.cmake._write_file")
    @patch("release_tool.cmake._load_file", return_value=CMAKE_CONTENT.format("0.1.2"))
    def test_set_new_version_without_change_doesnt_change(
        self, _mock_load_file, mock_write_file
    ):
        proj = _mock_load()
        proj.set_new_version("0.1.2")
        self.assertEqual("0.1.2", proj.version)
        mock_write_file.assert_called_with(
            "x", "CMakeLists.txt", CMAKE_CONTENT.format("0.1.2")
        )

    def test_current_version(self):
        proj = _mock_load()

        self.assertEqual(proj.version, "0.1.2")


def _mock_load():
    with patch(
        "release_tool.cmake._load_file", return_value=CMAKE_CONTENT.format("0.1.2")
    ):
        return CMakeProject("x")
