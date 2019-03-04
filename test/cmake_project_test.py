from release_tool.cmake import CMakeProject
import unittest
from unittest.mock import patch


class TestCMakeProject(unittest.TestCase):
    CMAKE_CONTENT = 'cmake_minimum_required(VERSION 3.14)\n\n' \
            'project(TestProj VERSION {})\n\n'

    def test_default_values(self):
        proj = CMakeProject('x')
        self.assertEqual(proj.name(), None)
        self.assertEqual(proj.current_version(), None)
        self.assertEqual(proj.path(), 'x')


    def test_load_reads_data(self):
        proj = CMakeProject('x/proj-a')

        with patch.object(proj, '_load_file', return_value=self.CMAKE_CONTENT.format('1.41.5')) as m:
            proj.load()

            self.assertEqual(proj.current_version(), '1.41.5')
            self.assertEqual(proj.name(), 'TestProj')

            m.assert_called_with(proj.path(), 'CMakeLists.txt')


    def test_store_writes_data(self):
        proj = self.__mock_load()
        proj.set_version('1.9.10')

        with patch.object(proj, '_load_file', return_value=self.CMAKE_CONTENT.format('0.0.1')) as m:
            with patch.object(proj, '_store_file') as m:
                proj.store()

                m.assert_called_with(proj.path(), 'CMakeLists.txt', self.CMAKE_CONTENT.format('1.9.10'))


    def test_current_version(self):
        proj = self.__mock_load()

        self.assertEqual(proj.current_version(), '0.1.2')


    def test_set_new_version(self):
        proj = self.__mock_load()

        self.assertEqual(proj.current_version(), '0.1.2')
        proj.set_version('1.3.4')
        self.assertEqual(proj.current_version(), '1.3.4')


    def __mock_load(self):
        proj = CMakeProject('x')

        with patch.object(proj, '_load_file', return_value=self.CMAKE_CONTENT.format('0.1.2')):
            proj.load()

        return proj


if __name__ == '__main__':
    unittest.main()
