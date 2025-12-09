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

import os
import abc
import git
from release_tool.cmake import CMakeProject
from release_tool.release_exception import ReleaseException


class UnsupportedProjectException(ReleaseException):
    pass


class ConditionFailedException(ReleaseException):
    pass


class Step(abc.ABC):
    @abc.abstractmethod
    def execute(self, proj, repo: git.Repo, new_version: str) -> None:
        raise NotImplementedError


class PreconditionStep(Step):
    def execute(self, proj, repo: git.Repo, new_version: str) -> None:
        if repo.is_dirty():
            raise ConditionFailedException("The project contains uncommited changes")
        if proj.version == new_version:
            raise ConditionFailedException("Version already up-to-date")


class UpdateVersionStep(Step):
    def execute(self, proj, repo: git.Repo, new_version: str) -> None:
        proj.set_new_version(new_version)


class CommitAndTagStep(Step):
    def __init__(self, message: str | None = None) -> None:
        self.__message = message if message else "Release v$v"

    def execute(self, proj, repo: git.Repo, new_version: str) -> None:
        commit_message = self.__message.replace("$v", new_version)
        repo.index.add([proj.PROJECT_CONFIG])
        repo.index.commit(commit_message)
        repo.create_tag(f"v{new_version}", message=commit_message)


class SetNextVersion(Step):
    def __init__(self, next_version: str) -> None:
        self.__next_version = next_version

    def execute(self, proj, repo: git.Repo, new_version: str) -> None:
        proj.set_new_version(self.__next_version)
        repo.index.add([proj.PROJECT_CONFIG])
        repo.index.commit("Prepare next iteration")


class ReleaseCycle:
    def __init__(self, proj, repo: git.Repo, steps: list) -> None:
        self.__proj = proj
        self.__repo = repo
        self.__steps = steps

    @classmethod
    def from_path(cls, path: str, steps: list):
        repo = git.Repo(path)

        if os.path.isfile(os.path.join(path, CMakeProject.PROJECT_CONFIG)):
            proj = CMakeProject(path)
            return cls(proj, repo, steps)
        raise UnsupportedProjectException(f"'{path}' no supported project found")

    def number_of_steps(self) -> int:
        return len(self.__steps)

    @property
    def repository(self) -> git.Repo:
        return self.__repo

    @property
    def project(self):
        return self.__proj

    def create_release(self, new_version: str):
        version = new_version.strip()
        for step in self.__steps:
            step.execute(self.__proj, self.__repo, version)
