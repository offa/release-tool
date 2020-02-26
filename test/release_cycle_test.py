
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
from unittest.mock import MagicMock, Mock, call, patch
import git
from release_tool.cmake import CMakeProject
from release_tool.release_cycle import ReleaseCycle, PreconditionStep, \
    UpdateVersionStep, CommitAndTagChangesStep, ConditionFailedException, \
    UnsupportedProjectException

class TestReleaseCycle(unittest.TestCase):

    @patch('os.path.isfile', return_value=True)
    def test_project_and_repository_from_path(self, _mock):
        with patch.object(git.Git, "__init__", lambda x, y: None):
            with patch.object(CMakeProject, "__init__", lambda x, y: None):
                cycle = ReleaseCycle.from_path("/tmp/cmake_project", [MagicMock()])
                self.assertIsInstance(cycle.project, CMakeProject)
                self.assertIsInstance(cycle.repository, git.Git)
                self.assertEqual(1, cycle.number_of_steps())

    @patch('os.path.isfile', return_value=False)
    def test_from_path_throws_if_no_project_file(self, _mock):
        with self.assertRaises(UnsupportedProjectException):
            ReleaseCycle.from_path("/tmp/cmake_project", [MagicMock()])
        _mock.assert_called_once_with("/tmp/cmake_project")

    def test_step_executed(self):
        proj = MagicMock()
        proj.version = "0.1.0"
        repo = MagicMock()
        step = MagicMock()

        cycle = ReleaseCycle(proj, repo, [step])
        cycle.create_release("0.1.1")

        self.assertEqual(1, step.execute.call_count)
        step.execute.assert_called_once_with(proj, repo, "0.1.1")

    def test_steps_executed_in_order(self):
        proj = MagicMock()
        proj.version = "6.7.7"
        repo = MagicMock()
        steps = [MagicMock(), MagicMock(), MagicMock()]

        cycle = ReleaseCycle(proj, repo, steps)

        expected_args = (proj, repo, "6.7.8")
        manager = Mock()
        (manager.step_0, manager.step_1, manager.step_2) = (steps[0], steps[1], steps[2])

        cycle.create_release("6.7.8")

        expected_calls = [call.step_0.execute(*expected_args),
                          call.step_1.execute(*expected_args),
                          call.step_2.execute(*expected_args),
                          ]
        self.assertEqual(expected_calls, manager.mock_calls)



class TestPreconditionStep(unittest.TestCase):

    # pylint: disable=R0201
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
        with self.assertRaises(ConditionFailedException):
            step.execute(proj, repo, "0.1.2")



class TestUpdateVersionStep(unittest.TestCase):

    # pylint: disable=R0201
    def test_sets_new_version(self):
        proj = MagicMock()
        repo = MagicMock()

        step = UpdateVersionStep()
        step.execute(proj, repo, "0.1.3")
        proj.set_new_version.assert_called_once_with("0.1.3")



class TestCommitAndTagChangesStep(unittest.TestCase):

    # pylint: disable=R0201
    def test_commits_changes_and_creates_tag(self):
        proj = MagicMock()
        repo = MagicMock()
        proj.version = "1.2.3"

        step = CommitAndTagChangesStep()
        step.execute(proj, repo, "1.2.3")
        repo.index.add.assert_called_once_with([proj.PROJECT_CONFIG])
        repo.index.commit.assert_called_once_with("Release v1.2.3.")
        repo.create_tag.assert_called_once_with("v1.2.3", message="Release v1.2.3.")
