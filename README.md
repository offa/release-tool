# Release Tool

[![CI](https://github.com/offa/release-tool/workflows/ci/badge.svg)](https://github.com/offa/release-tool/actions)
[![GitHub release](https://img.shields.io/github/release/offa/release-tool.svg)](https://github.com/offa/release-tool/releases)
[![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)](LICENSE)
![Python 3.9](https://img.shields.io/badge/python-3.9-green.svg)

Tool to create project releases of CMake based projects.

1. Check for uncommitted files
1. Update version info
1. Update Repository
    1. Commit version change
    1. Tag new version
1. *(Optional)* Set next version

## Usage

Use `releasetool --help` for a full list.

```bash
# Create a release 1.2.3 of the project in the current directory
releasetool -r 1.2.3

# Create a release 4.5.6 of the project in example/project directory
releasetool -r 4.5.6 example/project
```
