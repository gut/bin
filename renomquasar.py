#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

def main():
	from os import rename, path
	from sys import argv
	for i in argv[1:]:
		old = i.replace('pt-br','br').replace('-720p','').replace('-1080p','')
		# tira o ano, o imdb e separa decentemente o '-'
		str1 = ', '.join(old.split('-')[2:])
		parts = str1.split('.')
		# troca '.' por ' ', exceto o '.' da extensão
		nome = '%s.%s' % (' '.join(parts[:-1]), parts[-1],)
		# pronto! renomeia
		if path.isfile(i):
			print '"%s" => "%s"?' % (i, nome,)
			x = raw_input()
			if x == "":
				rename(i, nome)
			else:
				print 'Pulando...'
		else:
			print '%s não é arquivo!' % i

if __name__ == "__main__":
	main()

