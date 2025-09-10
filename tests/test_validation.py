import unittest
import sys
import os

# Add the parent directory to the sys.path to allow imports from the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import validate_data

class TestValidation(unittest.TestCase):

    def test_negative_input_fails_validation(self):
        """
        Test that validate_data returns an error for negative input values.
        """
        invalid_data = {"car": -100, "bus": 50, "energy": 200, "meat": 5, "veggie": 10}
        errors = validate_data(invalid_data)
        self.assertIn("Eingabewerte dürfen nicht negativ sein.", errors)

if __name__ == '__main__':
    unittest.main()
