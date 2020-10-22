# Test functions goes here
import unittest
import filecmp
from queue import PriorityQueue
from huffman import encode, decode, get_frequencies, generate_priorityqueue, convert_to_char

class TestHuffman(unittest.TestCase):

	def test_get_frequencies(self):
		expected_output = {'h':1,'i':1}
		actual_output=get_frequencies("hi")
		self.assertDictEqual(expected_output, actual_output)
		print("tested frequencies")

	def test_generate_priorityqueue(self):
		charcount = {'h':5,'i':4}
		myQueue = PriorityQueue()
		generate_priorityqueue(myQueue, charcount)
		first = myQueue.get()
		assert first[0] == 4
		second = myQueue.get()
		assert second[0] == 5
		print("tested priority order is corect or not")

	def test_convert_to_char(self):
		expected_result = "hi"
		original_result = convert_to_char("0110100001101001")
		assert original_result == expected_result

	def test_encode_decode(self):
		encode("story.txt", "story.huff")
		decode("story.huff", "story_.txt")
		assert(filecmp.cmp("story.txt","story_.txt"))
		print("Decoded file tested successfully")

if __name__ == '__main__':
	unittest.main()
