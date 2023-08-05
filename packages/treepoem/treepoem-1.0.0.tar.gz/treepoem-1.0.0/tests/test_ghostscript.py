import subprocess
import unittest


class GhostscriptTest(unittest.TestCase):

    def test_installed(self):
        process = subprocess.Popen(
            ['gs', '--version'],
            universal_newlines=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        self.assertEqual(process.returncode, 0)
        self.assertEqual(stderr, "")
        self.assertRegexpMatches(stdout, r'9\.\d\d')
