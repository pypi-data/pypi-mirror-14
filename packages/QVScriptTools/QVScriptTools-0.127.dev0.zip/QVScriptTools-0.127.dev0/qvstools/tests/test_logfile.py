import unittest, re, os
from qvstools.log import *

class TestBlock(unittest.TestCase):
	def setUp(self):
		print ("SETUP!")

	def tearDown(self):
		print ("TEAR DOWN!")

	def test_parse_logfile(self):
		print('Testing logfile parse.')
		logs = [
			r"qvstools\tests\testdata\DepsGraph1.qvw.log",
			r"qvstools\tests\testdata\DepsGraph2.qvw.log",
			r"qvstools\tests\testdata\DepsGraph3.qvw.log",
			r"qvstools\tests\testdata\ETLTubeData_Subbified.qvw.log"
			]
		
		for log in logs:
			lf = LogFile(log)

			for f in lf.get_file_lines():
				print(f['file'],' --> ',lf.find_file(f))

	def test_build_dependency_graph(self):
		test_input = r"qvstools\tests\testdata\DepsGraph3.qvw"
		deps = build_dependency_graph(test_input,depth=3,maxfiles=100)['triplets']
		for x in deps:
			print(x[0],x[2],x[4])

	def test_build_graphviz_graph(self):
		test_input = r"qvstools\tests\testdata\DepsGraph3.qvw"
		deps = build_dependency_graph(test_input,depth=3,maxfiles=100)
		with open('testoutput_graphvis.txt','w') as test_output:
			for q in deps['qvw']:
				test_output.write(q[0][0:-4] + ' [shape=box]\n')
			for q in deps['qvd']:
				test_output.write(q[0][0:-4] + ' [shape=ellipse]\n')
			for x in deps['triplets']:
				test_output.write('{0} -> {1} -> {2}\n'.format(x[0][0:-4],x[2][0:-4],x[4][0:-4]))


if __name__ == '__main__':
        unittest.main()

