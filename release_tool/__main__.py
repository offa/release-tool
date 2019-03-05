import argparse
import git
from .cmake import CMakeProject

def parse_args():
    parser = argparse.ArgumentParser(prog="release-tool",
                                     description='Performs releases')
    required = parser.add_argument_group('arguments')
    required.add_argument('--release-version', '-r', type=str,
                          help='Version to release')

    parser.add_argument('--version', '-v', action='version', version="%(prog)s 0.0.1",
                        help='Shows the program version')
    parser.add_argument("path", nargs=1)

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.release_version:
        print("ERROR: No Version")
        return

    path = args.path[0]
    repo = git.Repo(path)

    # Check Dirty
    if repo.is_dirty():
        print("ERROR: SCM Dirty")
        return # TODO: rtn code

    # Update Version
    proj = CMakeProject(path)
    proj.load()
    proj.set_version(args.release_version)
    proj.store()


    # Commit
    repo.index.add(["CMakeLists.txt"])
    repo.index.commit("Release v{}".format(proj.version()))
    # Tag
    repo.create_tag("v{}".format(proj.version()), message="Release v{}".format(proj.version()))


    # Done


if __name__ == '__main__':
    main()

