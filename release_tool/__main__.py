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

import argparse
import os
import git
from version import __version__
from cmake import CMakeProject
from release_cycle import ReleaseCycle, PreconditionStep, UpdateVersionStep, CommitAndTagChangesStep


class UnsupportedProjectException(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(prog="release-tool",
                                     description='Performs releases')
    required = parser.add_argument_group('arguments')
    required.add_argument('--release-version', '-r', type=str, required=True,
                          help='Version to release')
    parser.add_argument('--version', '-v', action='version',
                        version="%(prog)s {}".format(__version__),
                        help='Shows the program version')
    parser.add_argument("path", nargs=1)

    return parser.parse_args()


def project_contains_file(path, filename):
    return os.path.isfile(os.path.join(path, filename))


def init(path):
    repo = git.Repo(path)

    if project_contains_file(path, CMakeProject.PROJECT_CONFIG):
        proj = CMakeProject(path)
        return repo, proj
    raise UnsupportedProjectException("'{}' does not contain a supported project type".format(path))


def main():
    args = parse_args()

    new_version = args.release_version.strip()
    repo, proj = init(args.path[0])

    cycle = ReleaseCycle(proj, repo, [
        PreconditionStep(),
        UpdateVersionStep(),
        CommitAndTagChangesStep()
    ])
    cycle.create_release(new_version)


if __name__ == '__main__':
    main()
