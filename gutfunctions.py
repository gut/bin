#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

def listFilesRec(_dir = '.'):
	"""Retorna um generator de todos os arquivos e diretórios procurando
	recursivamente no diretório passado por parâmetro"""

	from os import path,listdir
	for f in listdir(_dir):
		file = path.join(_dir,f)
		if path.isdir(file):
			for k in listFilesRec(file):
				yield k
		yield file

def _listFilesRec(_dir = '.'):
	"""Retorna uma lista de todos os arquivos e diretórios procurando
	recursivamente no diretório passado por parâmetro"""
	from os import path,listdir
	files = []
	for f in listdir(_dir):
		file = path.join(_dir,f)
		if path.isdir(file):
			for k in _listFilesRec(file):
				files.append(k)
		files.append(file)
	return files

def listDirsRec(_dir = '.', inicio = True):
	"""Retorna uma lista de todos os diretórios procurando
	recursivamente no diretório passado por parâmetro"""
	from os import path,listdir
	dirs = [_dir,] if inicio else []  # incluindo o primeiro diretório
	for f in listdir(_dir):
		file = path.join(_dir,f)
		if path.isdir(file):
			dirs.append(file)
			for k in listDirsRec(file, False):
				dirs.append(k)
	return dirs

def listFilesRecNested(_dir = '.'):
	"""Retorna uma lista de todos os arquivos, sendo a primeira
	posição da lista uma string com o nome do diretório corrente e
	se for encontrado um subdiretório haverá uma lista recursiva."""

	from os import path,listdir,chdir
	files = [_dir,]
	chdir(_dir)
	for file in listdir('.'):
		if path.isdir(file):
			files.append(listFilesRecNested(file))
		else:
			files.append(file)
	if _dir != '.':
		chdir('..')
	return files

def lenRec(l = [], comAgrupamentos = False):
	"""Retorna o tamanho de uma lista, tupla ou dicionário, agindo
	recursivamente e retornando o número de átomos"""
	x = 0
	for i in l:
		if type(i) in (list, tuple, dict):
			x += lenRec(i, comAgrupamentos)
			if comAgrupamentos:
				x += 1  # contabiliza também esse elemento
		else:
			x += 1
	return x

####
# Cores
####

def __pegaCor(cor):
	# de http://aurelio.net/shell/canivete.html#cores
	if cor == 'amarelo':
		return '\x1b[01;33m'
	elif cor == 'azul':
		return '\x1b[01;34m'
	elif cor == 'branco':
		return '\x1b[00m'
	elif cor == 'cinza':
		return '\x1b[01;30m'
	elif cor == 'verde':
		return '\x1b[01;32m'
	elif cor == 'vermelho':
		return '\x1b[01;31m'

def mudaCor(cor):
	print corString(cor, '', voltaBranco = False)

def corString(cor, s, voltaBranco = True):
	c = __pegaCor(cor)
	f = __pegaCor('branco') if voltaBranco else ''
	return '%s%s%s' % (c, s, f)

if __name__ == "__main__":
	a = [1,2,3]
	print "3 vai ser: ",lenRec(a)
	b = [0,a,5]
	print "5 vai ser: ",lenRec(b)
	print "6 vai ser: ",lenRec(b, True)
	c = [1,[2,[3]]]
	print "5 vai ser: ",lenRec(c, True)
	d = [[[[1]],2],3]
	print "6 vai ser: ",lenRec(d, True)
