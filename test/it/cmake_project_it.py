from release_tool.cmake import CMakeProject
import unittest

class CMakeProjectIT(unittest.TestCase):

    def test_loading_project_file(self):
        proj = CMakeProject('test/it/data')
        proj.load()

        self.assertEqual(proj.name(), 'IntegrationTest')
        self.assertEqual(proj.current_version(), '1.8.9')



if __name__ == '__main__':
    unittest.main()

