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

import contextlib
import io
import unittest
from argparse import Namespace
from unittest.mock import patch

import git

from release_tool import __main__
from release_tool.release_cycle import ConditionFailedException


class TestMainErrorHandling(unittest.TestCase):
    def test_git_error_is_handled(self) -> None:
        output = self._run_main_with_error(git.InvalidGitRepositoryError("/no/repo"))

        self.assertTrue(output.startswith("ERROR:"))
        self.assertIn("/no/repo", output)

    def test_value_error_is_handled(self) -> None:
        output = self._run_main_with_error(
            ValueError("Invalid project(...): 'CMakeLists.txt'")
        )

        self.assertTrue(output.startswith("ERROR:"))

    def test_os_error_is_handled(self) -> None:
        output = self._run_main_with_error(FileNotFoundError("CMakeLists.txt"))

        self.assertTrue(output.startswith("ERROR:"))

    def test_release_exception_is_handled(self) -> None:
        output = self._run_main_with_error(
            ConditionFailedException("The project contains uncommited changes")
        )

        self.assertTrue(output.startswith("ERROR:"))

    def _run_main_with_error(self, error: Exception) -> str:
        with (
            patch("release_tool.__main__.parse_args", return_value=_args()),
            patch("release_tool.__main__.ReleaseCycle.from_path", side_effect=error),
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            try:
                __main__.main()
            except SystemExit as sys_exit:
                self.assertEqual(1, sys_exit.code)
            else:
                self.fail("main() did not exit")

        return stdout.getvalue()


def _args() -> Namespace:
    return Namespace(
        release_version="1.2.3",
        path="/tmp/cmake_project",
        message=None,
        next_version=None,
    )
