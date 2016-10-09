#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

def main(argv = [__name__,]):
	if len(argv) != 3:
		print "arg1 = texto a ser procurado"
		print "arg2 = arquivo com a lista dos arquivos a procurar"
		print ' '.join(["Resultado: próxima palavra após o texto procurado em",
			"cada um dos arquivos da lista"])
		return

	found = []
	token = argv[1]
	print "Verificando '%s' nos arquivos..." % token,
	for file in open(argv[2]).read().splitlines():
		for linenb, content in enumerate(open(file).read().splitlines()):
			# verifica se em algum lugar tem esse texto da função escrito
			pos = content.find(token, 0)
			while pos > -1:  # abaixo para várias ocorrências no mesmo arquivo
				cut = pos + len(token)
				subpos = 1
				try:
					while not content[cut+subpos] in [' ','(','\n',',',':']: # separadores
						subpos +=1
				except IndexError:
					subpos -= 1  # acabou a string, ok, pega até ae
				new = content[cut:cut+subpos].strip()
				# adiciona apenas se não tiver (der erro)
				try:
					found.index(new)
				except ValueError:
					found.append(new)
				pos = content.find(token, pos+1)  # procurando a próxima
	if found:  # se houver algum objeto aqui
		print "\nAchou isso nos arquivos: (%d)" % len(found)
		print ', '.join(found)

if __name__ == "__main__":
	from sys import argv
	main(argv)

