#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

def main(argv = [__name__,]):
	from os import path, chmod, system
	from progressbar import ProgressBar
	from gutfunctions import _listFilesRec

	print "Aguarde, gerando lista de arquivos a serem processados...",
	if argv[1:]:
		files = _listFilesRec(argv[1:])
	else:
		files = _listFilesRec()
	if not files:
		print 'Nenhum arquivo a ser processado!'
		return
	print 'pronto'
	p = ProgressBar(len(files))
	dirs = comum = 0
	for n, i in enumerate(files):
		p.setStatus(n, i)
		if path.isdir(i):  # or not system('file %s | grep executable > /dev/null' % i):
			dirs += 1
			chmod(i, 0775)  # rwxr-xr-x para diretórios  #e executáveis
		else:
			comum += 1
			chmod(i, 0664)  # rw-r--r-- para arquivos comuns
	p.setEnd()
	print '%d arquivos processados, desses: %d diretórios e %d arquivos comuns' % (
		p.getTotalSteps(), dirs, comum,)



if __name__ == "__main__":
	from sys import argv
	main(argv)

