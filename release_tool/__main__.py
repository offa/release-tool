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


def main():
    args = parse_args()

    path = args.path[0]
    repo = git.Repo(path)
    proj = CMakeProject(path)
    proj.load()

    ensure_condition(not repo.is_dirty(), 'The project contains uncommited changes')
    ensure_condition(proj.version() != args.release_version, "Version already up-to-date")

    # Update Version
    proj.set_version(args.release_version)
    proj.store()


    # Commit
    repo.index.add([proj.project_config()])
    ensure_condition(repo.is_dirty(), 'No changes to commit')
    repo.index.commit("Release v{}".format(proj.version()))
    repo.create_tag("v{}".format(proj.version()), message="Release v{}".format(proj.version()))



if __name__ == '__main__':
    main()

