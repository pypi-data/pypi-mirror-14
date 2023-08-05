from tests.helper import ExternalVersionTestCase


class PyPITest(ExternalVersionTestCase):
    def test_pypi(self):
        self.assertEqual(self.sync_get_version("example", {"pypi": None}), "0.1.0")
