
from unittest import TestCase
from pytmp.pytmp import tmp_clear, tmp_create, tmp_delete, tmp_items, tmp_keys, tmp_read, tmp_update


class PytmpTest(TestCase):

	def setUp(self):
		tmp_create('str', 'hello world')
		tmp_create('int', 1)
		tmp_create('float', 1.5)
		tmp_create('list', ['a', 'b', 'c'])
		tmp_create('dict', {'name': 'Paulo Roberto'})

	def test_str(self):
		self.assertEqual(type(tmp_read('str')), str)

	def test_int(self):
		self.assertEqual(type(tmp_read('int')), int)

	def test_float(self):
		self.assertEqual(type(tmp_read('float')), float)

	def test_list(self):
		self.assertEqual(type(tmp_read('list')), list)

	def test_dict(self):
		self.assertEqual(type(tmp_read('dict')), dict)

	def test_items(self):
		self.assertEqual(5, len(tmp_items()))

	def test_keys(self):
		self.assertEqual(5, len(tmp_keys()))

	def test_read_str(self):
		self.assertEqual(tmp_read('str'), 'hello world')

	def test_read_int(self):
		self.assertEqual(1, tmp_read('int'))

	def test_read_float(self):
		self.assertEqual(1.5, tmp_read('float'))

	def test_read_list(self):
		self.assertEqual(['a', 'b', 'c'], tmp_read('list'))

	def test_read_dict(self):
		self.assertEqual({'name': 'Paulo Roberto'}, tmp_read('dict'))

	def test_update(self):
		self.assertEqual('world hello', tmp_update('str', 'world hello'))

	def test_delete(self):
		self.assertEqual(True, tmp_delete('str'))

	def test_delete_not_found(self):
		self.assertEqual(False, tmp_delete('key_not_exist'))

	def test_clear(self):
		self.assertEqual([], tmp_clear())
