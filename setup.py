import setuptools
from release_tool.version import __version__


def long_description_readme():
    with open("README.md", "r", encoding="utf-8") as readme_file:
        return readme_file.read()


setuptools.setup(
    name='release-tool',
    version=__version__,
    author='offa',
    author_email='offa@github',
    description='Tool to create project releases.',
    long_description=long_description_readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/offa/release-tool',
    packages=['release_tool'],
    entry_points={"console_scripts": ["releasetool = release_tool.__main__:main"]},
    keywords=['project', 'release', 'cmake', 'git'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    install_requires=['GitPython == 3.1.26']
)
