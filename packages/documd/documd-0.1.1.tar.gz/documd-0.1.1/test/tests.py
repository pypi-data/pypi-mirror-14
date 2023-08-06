import unittest
import os
from documd import documentation
import example


OUTPUT_PATH = '.'
OUTPUT_EXAMPLE = './output_example.md'


class CliTestCase(unittest.TestCase):

    def test_generate_markdown(self):
        documentation.generate(output_path=OUTPUT_PATH)
        with open(os.path.join(OUTPUT_PATH, 'test.md'), 'r') as generated_file:
            generated_result = generated_file.read()
        with open(OUTPUT_EXAMPLE, 'r') as example_file:
            example_result = example_file.read()
        self.assertEqual(generated_result, example_result)
