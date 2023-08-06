import os
import unittest
from test.test_support import EnvironmentVarGuard
from baiji.util import tempfile

class TestTempfile(unittest.TestCase):

    def test_that_NamedTemporaryFile_honors_TMP_env_var(self):
        env = EnvironmentVarGuard()
        env.set('BAIJI_TMP', '.')
        with env:
            with tempfile.NamedTemporaryFile('w') as tf:
                self.assertEquals(os.path.dirname(tf.name), os.getcwd())
