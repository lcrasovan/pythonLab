import unittest

class TestNumberMethods(unittest.TestCase):

    def test_adding_one_with_one_equals_two(self):
        self.assertEqual(1 + 1, 2)

    def test_adding_floating_one_with_floating_one_equals_floating_two(self):
        self.assertEqual(1.0 + 1.0, 2.0)
        
    def test_adding_floating_one_with_integer_one_equals_floating_two_or_integer_two(self):
        self.assertEqual(1.0 + 1, 2) 
        self.assertEqual(1.0 + 1, 2.0)        

if __name__ == '__main__':
    unittest.main(verbosity=2)