import setuptools

def long_description_readme():
    with open("README.md", "r") as readme_file:
        return readme_file.read()


setuptools.setup(
    name='release-tool',
    version='0.0.1',
    author='offa',
    author_email='offa@github',
    description='Tool to create project releases.',
    long_description=long_description_readme(),
    url='https://github.com/offa/release-tool',
    packages=setuptools.find_packages(),
    keywords=['project', 'release', 'cmake', 'git'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
