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

import unittest
from unittest.mock import MagicMock, Mock, call, patch
import git
from release_tool.cmake import CMakeProject
from release_tool.release_cycle import ReleaseCycle, PreconditionStep, \
    UpdateVersionStep, CommitAndTagStep, ConditionFailedException, \
    UnsupportedProjectException


class TestReleaseCycle(unittest.TestCase):

    @patch('os.path.isfile', return_value=True)
    def test_project_and_repository_from_path(self, mock):
        with patch.object(git.Repo, "__init__", lambda p0, p1: None), \
                patch.object(CMakeProject, "__init__", lambda p0, p1: None):
            cycle = ReleaseCycle.from_path("/tmp/cmake_project", [MagicMock()])
            mock.assert_called_once_with("/tmp/cmake_project/CMakeLists.txt")
            self.assertIsInstance(cycle.project, CMakeProject)
            self.assertIsInstance(cycle.repository, git.Repo)
            self.assertEqual(1, cycle.number_of_steps())

    @patch('os.path.isfile', return_value=False)
    def test_from_path_throws_if_no_project_file(self, mock):
        with patch.object(git.Repo, "__init__", lambda p0, p1: None):
            with self.assertRaises(UnsupportedProjectException):
                ReleaseCycle.from_path("/tmp/cmake_project", [MagicMock()])
        mock.assert_called_once_with("/tmp/cmake_project/CMakeLists.txt")

    def test_step_executed(self):
        proj, repo = _create_mocks("0.1.0")
        step = MagicMock()

        cycle = ReleaseCycle(proj, repo, [step])
        cycle.create_release("0.1.1")

        self.assertEqual(1, step.execute.call_count)
        step.execute.assert_called_once_with(proj, repo, "0.1.1")

    def test_steps_executed_in_order(self):
        proj, repo = _create_mocks("6.6.7")
        steps = [MagicMock(), MagicMock(), MagicMock()]

        cycle = ReleaseCycle(proj, repo, steps)

        expected_args = (proj, repo, "6.7.8")
        manager = Mock()
        (manager.step_0, manager.step_1, manager.step_2) = (steps[0], steps[1], steps[2])

        cycle.create_release("6.7.8")

        expected_calls = [
            call.step_0.execute(*expected_args),
            call.step_1.execute(*expected_args),
            call.step_2.execute(*expected_args)
        ]
        self.assertEqual(expected_calls, manager.mock_calls)

    def test_create_release_strips_whitespaces(self):
        proj, repo = _create_mocks("0.1.0")
        step = MagicMock()

        cycle = ReleaseCycle(proj, repo, [step])
        cycle.create_release("\t\n 0.3.4  ")

        self.assertEqual(1, step.execute.call_count)
        step.execute.assert_called_once_with(proj, repo, "0.3.4")


class TestPreconditionStep(unittest.TestCase):

    def test_passes_if_repo_not_dirty(self):
        proj, repo = _create_mocks("0.1.2")
        repo.is_dirty = MagicMock(return_value=False)

        step = PreconditionStep()
        step.execute(proj, repo, "0.1.3")

    def test_fails_if_repo_dirty(self):
        proj, repo = _create_mocks("0.1.2")
        repo.is_dirty = MagicMock(return_value=True)

        step = PreconditionStep()
        with self.assertRaises(Exception):
            step.execute(proj, repo, "0.1.3")

    def test_passes_if_different_version(self):
        proj, repo = _create_mocks("0.1.2")
        repo.is_dirty = MagicMock(return_value=False)

        step = PreconditionStep()
        step.execute(proj, repo, "0.1.3")

    def test_fails_if_same_version(self):
        proj, repo = _create_mocks("0.1.2")
        repo.is_dirty = MagicMock(return_value=False)

        step = PreconditionStep()
        with self.assertRaises(ConditionFailedException):
            step.execute(proj, repo, "0.1.2")


class TestUpdateVersionStep(unittest.TestCase):

    def test_sets_new_version(self):
        proj, repo = _create_mocks("0.0.1")

        step = UpdateVersionStep()
        step.execute(proj, repo, "0.1.3")
        proj.set_new_version.assert_called_once_with("0.1.3")


class TestCommitAndTagStep(unittest.TestCase):

    def test_commits_changes_and_creates_tag(self):
        proj, repo = _create_mocks("1.2.3")

        step = CommitAndTagStep()
        step.execute(proj, repo, "1.2.3")
        repo.index.add.assert_called_once_with([proj.PROJECT_CONFIG])
        repo.index.commit.assert_called_once_with("Release v1.2.3")
        repo.create_tag.assert_called_once_with("v1.2.3", message="Release v1.2.3")

    def test_commits_changes_and_creates_tag_with_message(self):
        proj, repo = _create_mocks("1.2.3")

        step = CommitAndTagStep("Custom message for version '$v'")
        step.execute(proj, repo, "1.2.3")
        repo.index.add.assert_called_once_with([proj.PROJECT_CONFIG])
        repo.index.commit.assert_called_once_with("Custom message for version '1.2.3'")
        repo.create_tag.assert_called_once_with("v1.2.3",
                                                message="Custom message for version '1.2.3'")


def _create_mocks(version):
    proj = MagicMock()
    repo = MagicMock()
    proj.version = version
    return (proj, repo)
