#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet <gsscalet@gmail.com>
Licença: GPLv3 ou mais recente
"""

__VERSION__ = "0.2.3"

def tester(cmdList, numint, verbose = False, quiet = False):
	u"""
	Script feito para fazer benchmarks.
	Através do comando e do número de interações o script utiliza o binário
	time para checar os tempos. Pega os valores "real" do time e monta
	algumas estatísticas, como o desvio padrão.
	"""
	medias = {}
	erros = {}
	for cmdRaw in cmdList:
		cmd = 'time %s' % cmdRaw

		import subprocess, re, math, sys
		# funciona para até 1 minuto
		regex = re.compile('real\t0m([^s]*)s')
		tempo = []
		print corString("verde","Comando:"), cmd
		for i in range(numint):
			if not quiet:
				print corString("verde","Interação %d:" % i),
			sys.stdout.flush()
			p = subprocess.Popen(cmd,  shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
			stderr = p.stderr.read()
			stdout = p.stdout.read()
			res = regex.search(stderr)
			if res:
				tempo.append(float(res.groups()[0]))
				if not quiet:
					print "demorou %.3f s" % tempo[-1]
				if verbose:
					print corString("verde", "Stdout:"), stdout
					print corString("verde", "Stderr:"), stderr
			else:
				print "erro! Não foi possível parsear a saída do time (o comando foi executado?)"
		tempo.sort()
		media = sum(tempo)/len(tempo)
		sd = math.sqrt(
				sum(
					[(i - media)**2 for i in tempo]
				)
				/(len(tempo)-1)
			)
		medias[cmdRaw] = media
		erros[cmdRaw] = sd
		if not quiet:
			print '\nAmostragem ordenadada crescentemente:'
			print ' '.join(['%.3f' % i for i in tempo])
			print corString("verde",'Média:'), '%.3f' % (media)
			print corString("verde",'Mediana:'), '%.3f' % tempo[int(len(tempo)/2)]
			print corString("verde",'Desvio Padrão:'), '%.6f' % (sd)
			print corString("azul",'=============================================\n')

	print corString("azul",'\n=============================================')
	print "Resumão de", corString("verde", str(numint)), "amostras:"
	for cmd in cmdList:
		print "%s: %.3f +- %.6f" % (corString("verde", cmd), medias[cmd], erros[cmd])
	print corString("azul",'=============================================')

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
	from sys import argv, exit
	from os import sep
	from optparse import OptionParser

	usage = u"usage: %prog [--verbose] CMD NUM"
	example = u"""Detalhe: Coloque o parâmetro CMD como uma string, por exemplo:
	%s "mpg123 -t aerosmith.mp3" 40""" % (argv[0])

	parser = OptionParser(usage,
			description=(tester.__doc__.replace('\t','') + example),
			version="%%prog %s" % __VERSION__)
	parser.add_option('-v', '--verbose', dest='verbose', action="store_true",
		default=False, help=u"Mostra saída de padrão e de erros da execução")
	parser.add_option('-q', '--quiet', dest='quiet', action="store_true",
		default=False, help=u"Mostra apenas o resultado do benchmark no final")

	if len(argv) == 1 or len(argv) == 2 and argv[1] not in ('-h', '--help', '--version'):
		#not enough arguments
		print """ERROR: not enough arguments.
Try `%s --help' for more information""" % argv[0].split(sep)[-1]
		exit(1)

	(opt, args) = parser.parse_args(argv[1:])
	verbose = opt.verbose
	quiet = opt.quiet
	try:
		par2 = int(args[-1])
	except:
		print "O número de interações deve ser inteiro"
		exit(2)
	if par2 < 2:
		print "Número de interações muito baixo, tente ao menos 2"
		exit(3)
	tester(args[:-1], par2, verbose, quiet)

