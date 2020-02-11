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


class UnsupportedProjectException(Exception):
    pass


class ConditionFailedException(Exception):
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


def ensure_condition(condition, message):
    if not condition:
        raise ConditionFailedException(message)


def project_contains_file(path, filename):
    return os.path.isfile(os.path.join(path, filename))


def init(path):
    repo = git.Repo(path)

    if project_contains_file(path, CMakeProject.project_config()):
        proj = CMakeProject(path)
        proj.load()
        return repo, proj
    raise UnsupportedProjectException("'{}' does not contain a supported project type".format(path))


def check_precondition(repo, proj, new_version):
    ensure_condition(not repo.is_dirty(), 'The project contains uncommited changes')
    ensure_condition(proj.version() != new_version, "Version already up-to-date")


def update_version_config(proj, new_version):
    proj.set_version(new_version)
    proj.store()


def update_scm(repo, proj, new_version):
    repo.index.add([proj.project_config()])
    ensure_condition(repo.is_dirty(), 'No changes to commit')

    commit_message = "Release v{}".format(new_version)
    repo.index.commit(commit_message)
    repo.create_tag("v{}".format(new_version), message=commit_message)


def main():
    args = parse_args()

    new_version = args.release_version.strip()
    repo, proj = init(args.path[0])

    check_precondition(repo, proj, new_version)
    update_version_config(proj, new_version)
    update_scm(repo, proj, new_version)


if __name__ == '__main__':
    main()
