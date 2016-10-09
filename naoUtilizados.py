#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

def main(argv = [__name__,]):
	if len(argv) != 3:
		print "arg1 = arquivo com listas dos nomes das funções"
		print "arg2 = arquivo com a lista dos arquivos a procurar"
		print ' '.join(["Resultado: funções que não foram referenciadas em nenhum dos"
			"arquivos (excluindo os resultados que foram referenciados com 'def ' ou"
			"'class ' antes)"])
		return

	notReferenced = []
	for func in open(argv[1]).read().splitlines():
		flag = False
		print "Verificando a função %s nos arquivos..." % func,
		for file in open(argv[2]).read().splitlines():
			for linenb, content in enumerate(open(file).read().splitlines()):
				# verifica se em algum lugar tem esse texto da função escrito
				pos = content.find(func, 0)
				while pos > -1:  # abaixo para várias ocorrências no mesmo arquivo
					_def = content[pos - len('def '):pos] == 'def '  # tem def antes?
					_class = content[pos - len('class '):pos] == 'class '  # tem class antes?
					if not _def and not _class:
						flag = '%s:%d' % (file, linenb)  # não achamos nada! vai pra lista
					pos = content.find(func, pos+1)  # procurando a próxima
		if flag:
			print " achou referência (i.e %s)" % flag
		else:
			# essa função não foi achada em lugar algum
			print " não achou nada!"
			notReferenced.append(func)
	if notReferenced:  # se houver algum objeto aqui
		print "\nFunções não referenciadas nos arquivos: (%d)" % len(notReferenced),
		print ', '.join(notReferenced)

if __name__ == "__main__":
	from sys import argv
	main(argv)

