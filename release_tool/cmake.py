import os
import re

class CMakeProject():

    def __init__(self, proj_dir):
        self.__proj_dir = proj_dir
        self.__version = None
        self.__name = None


    def load(self):
        content = self._load_file(self.__proj_dir, 'CMakeLists.txt')
        m = re.search('project\\((.+?) VERSION (.+?)\\)', content)

        self.__name = (m.group(1))
        self.set_version(m.group(2))


    def name(self):
        return self.__name


    def current_version(self):
        return self.__version;


    def set_version(self, new_version):
        self.__version = new_version


    def _load_file(self, path, file):
        with open(os.path.join(path, file)) as f:
            return f.read()
        return None


