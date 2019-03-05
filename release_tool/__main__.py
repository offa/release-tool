import sys
import argparse
import git
from .cmake import CMakeProject


def parse_args():
    parser = argparse.ArgumentParser(prog="release-tool",
                                     description='Performs releases')
    required = parser.add_argument_group('arguments')
    required.add_argument('--release-version', '-r', type=str, required=True,
                          help='Version to release')

    parser.add_argument('--version', '-v', action='version', version="%(prog)s 0.0.1",
                        help='Shows the program version')
    parser.add_argument("path", nargs=1)

    return parser.parse_args()


def ensure_condition(condition, message):
    if not condition:
        print("{}".format(message))
        sys.exit(1)


def init(path):
    repo = git.Repo(path)
    proj = CMakeProject(path)
    proj.load()

    return repo, proj


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

