
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
from release_tool.release_cycle import PreconditionStep, UpdateVersionStep, CommitAndTagChangesStep

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



class TestUpdateVersionStep(unittest.TestCase):

    def test_sets_new_version(self):
        proj = MagicMock()
        repo = MagicMock()

        step = UpdateVersionStep()
        step.execute(proj, repo, "0.1.3")
        proj.set_new_version.assert_called_once_with("0.1.3")



class TestCommitAndTagChangesStep(unittest.TestCase):

    def test_commits_changes_and_creates_tag(self):
        proj = MagicMock()
        repo = MagicMock()
        proj.version = "1.2.3"

        step = CommitAndTagChangesStep()
        step.execute(proj, repo, "1.2.3")
        repo.index.commit.assert_called_once_with("Release v1.2.3.")
        repo.create_tag.assert_called_once_with("v1.2.3", message="Release v1.2.3.")
