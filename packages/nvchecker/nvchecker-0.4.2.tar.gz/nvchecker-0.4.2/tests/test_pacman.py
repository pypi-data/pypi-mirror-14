import shutil
import pytest
from tests.helper import ExternalVersionTestCase


@pytest.mark.skipif(shutil.which("pacman") is None,
                    reason="requires pacman command")
class PacmanTest(ExternalVersionTestCase):
    def test_pacman(self):
        self.assertEqual(self.sync_get_version("ipw2100-fw", {"pacman": None}), "1.3-7")

    def test_pacman_strip_release(self):
        self.assertEqual(self.sync_get_version("ipw2100-fw", {"pacman": None, "strip-release": 1}), "1.3")
