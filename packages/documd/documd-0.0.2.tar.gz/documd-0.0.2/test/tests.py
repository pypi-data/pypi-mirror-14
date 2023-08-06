import unittest
from documd import documentation
import example


OUTPUT_FILE = './test.md'
OUTPUT_EXAMPLE = './output_example.md'


class CliTestCase(unittest.TestCase):

    def test_generate_markdown(self):
        documentation.generate(output_file=OUTPUT_FILE)
        with open(OUTPUT_FILE, 'r') as generated_file:
            generated_result = generated_file.read()
        with open(OUTPUT_EXAMPLE, 'r') as example_file:
            example_result = example_file.read()
        self.assertEqual(generated_result, example_result)
