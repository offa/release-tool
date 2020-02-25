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


class ConditionFailedException(Exception):
    pass


class PreconditionStep:

    # pylint: disable=R0201
    def execute(self, proj, repo, new_version):
        if repo.is_dirty():
            raise ConditionFailedException("The project contains uncommited changes")
        if proj.version == new_version:
            raise ConditionFailedException("Version already up-to-date")


class UpdateVersionStep:

    # pylint: disable=R0201
    def execute(self, proj, _repo, new_version):
        proj.set_new_version(new_version)


class CommitAndTagChangesStep:

    # pylint: disable=R0201
    def execute(self, proj, repo, new_version):
        commit_message = "Release v{}.".format(new_version)
        repo.index.add([proj.PROJECT_CONFIG])
        repo.index.commit(commit_message)
        repo.create_tag("v{}".format(new_version), message=commit_message)


class ReleaseCycle:

    def __init__(self, proj, repo, steps):
        self.__proj = proj
        self.__repo = repo
        self.__steps = steps

    def create_release(self, new_version):
        for step in self.__steps:
            step.execute(self.__proj, self.__repo, new_version)
