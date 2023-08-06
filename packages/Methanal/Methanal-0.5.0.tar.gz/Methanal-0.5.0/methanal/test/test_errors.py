from twisted.trial import unittest

from methanal import errors



class DeprecationWarningsTests(unittest.TestCase):
    """
    Tests for L{methanal.errors} module deprecation warnings.
    """
    def test_invalidEnumItem(self):
        """
        L{methanal.errors.InvalidEnumItem} is deprecated.
        """
        errors.InvalidEnumItem
        warnings = self.flushWarnings([self.test_invalidEnumItem])
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]['category'], DeprecationWarning)
        self.assertIn(
            'methanal.errors.InvalidEnumItem was deprecated in Methanal 0.4.0',
            warnings[0]['message'])
