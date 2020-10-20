# Test functions goes here
import unittest

from huffman import encode, decode

class TestHuffman(unittest.TestCase):
	# write all your tests here
	# function name should be prefixed with 'test'

	def test_encode(self):
		encode("file.txt", "testt.huff")
		assert True

	def test_decode(self):
		decode("testt.huff", "file_.txt")
		assert True

if __name__ == '__main__':
	unittest.main()
