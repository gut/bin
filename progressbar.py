#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

import sys
_barSize = 50  # chars
_textSize = 50

class ProgressBar:
	"""Flexible ProgressBar made on ascii"""

	def __init__(self, totalSteps):
		self.total = float(totalSteps)
		self.step = 0
		print ''  # \n para inicializar
		self.printBar()

	def printBar(self):
		print '\r',
		sys.stdout.write('[%s] %03.1f%% ' % (
			('=' * self.step + '>').ljust(_barSize + 1),
			100*(self.step / float(_barSize))
		))
		sys.stdout.flush()

	def normalized(self, i):
		from math import floor
		return int(floor(_barSize*(i / self.total)))

	def setStatus(self, i, text = None):
		new = self.normalized(i)
		if new - self.step >= 1:
			# está na hora de atualizar
			self.step = new
			self.printBar()
			if text:
				if len(text) > _textSize:
					print (text[:_textSize - 3] + '...').ljust(_textSize),
				else:
					print (text[:_textSize]).ljust(_textSize),
				sys.stdout.flush()

	def setEnd(self):
		self.setStatus(self.total)
		print ''  # \n para finalizar

	def getTotalSteps(self):
		return self.total

def main(argv = [__name__,]):
	from time import sleep
	total = 100
	p = ProgressBar(total)
	for i in range(total):
		p.setStatus(i, chr(28 + i))
		sleep(.05)
	p.setEnd()

if __name__ == "__main__":
	from sys import argv
	main(argv)

