import os
import re

class CMakeProject():
    __PATTERN = 'project\\((.+?) VERSION (.+?)\\)'

    def __init__(self, proj_dir):
        self.__proj_dir = proj_dir
        self.__version = None
        self.__name = None


    def path(self):
        return self.__proj_dir


    def name(self):
        return self.__name


    def version(self):
        return self.__version;


    def project_config(self):
        return 'CMakeLists.txt'


    def set_version(self, new_version):
        self.__version = new_version


    def load(self):
        content = self._load_file(self.__proj_dir, 'CMakeLists.txt')
        m = re.search(self.__PATTERN, content)

        self.__name = (m.group(1))
        self.set_version(m.group(2))


    def store(self):
        content = self._load_file(self.__proj_dir, 'CMakeLists.txt')
        updated = r'project(\1 VERSION {})'.format(self.version())
        result = re.sub(self.__PATTERN, updated, content)

        self._store_file(self.__proj_dir, 'CMakeLists.txt', result)


    def _load_file(self, path, file):
        with open(os.path.join(path, file)) as f:
            return f.read()
        return None


    def _store_file(self, path, file, content):
        with open(os.path.join(path, file), 'w') as f:
            f.write(content)


