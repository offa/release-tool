
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
from unittest.mock import MagicMock
from release_tool.release_cycle import PreconditionStep

class TestPreconditionStep(unittest.TestCase):

    def test_passes_if_repo_not_dirty(self):
        proj = MagicMock()
        proj.version = "0.1.2"
        repo = MagicMock()
        repo.is_dirty = MagicMock(return_value=False)

        step = PreconditionStep()
        step.execute(proj, repo, "0.1.3")

    def test_fails_if_repo_dirty(self):
        proj = MagicMock()
        proj.version = "0.1.2"
        repo = MagicMock()
        repo.is_dirty = MagicMock(return_value=True)

        step = PreconditionStep()
        with self.assertRaises(Exception):
            step.execute(proj, repo, "0.1.3")

    def test_passes_if_different_version(self):
        proj = MagicMock()
        repo = MagicMock()
        repo.is_dirty = MagicMock(return_value=False)
        proj.version = "0.1.2"

        step = PreconditionStep()
        step.execute(proj, repo, "0.1.3")

    def test_fails_if_same_version(self):
        proj = MagicMock()
        repo = MagicMock()
        repo.is_dirty = MagicMock(return_value=False)
        proj.version = "0.1.2"

        step = PreconditionStep()
        with self.assertRaises(Exception):
            step.execute(proj, repo, "0.1.2")
