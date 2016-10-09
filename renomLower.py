#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

__VERSION__ = 1.2
from structure import File, Directory

def renomLower(argv = [__name__,]):
    u"""Renomeia todos os arquivos e subdiretórios para minúsculo,
    recursivamente. Confirma a cada arquivo e só é abortado com sinais"""
    from os import path
    global total

    if len(argv) > 2:
        import sys
        print "O que que eu faço com tanto argumento?!\nVeja como isso funciona",
        print "digitando `%s --help'" % sys.argv[0]
        sys.exit(1)
    elif len(argv) == 2:
        folder = path.isfile(argv[1])
    else:
        folder = '.'
    files = Directory(folder)
    print files
    return
    total = files.totalLength()
    a = renomRec(files, folder)
    if a == total:
        print "Ok!"

def renomRec(files, lastdir, atual = 0, level = 0):
    """Level indica a identação (profundidade) da pasta a ser trabalhada"""
    from os import path, rename
    global verbose, sagaz, capitaliza, total

    if files.dirname != '.':
        basedir = path.join(lastdir, files.dirname)
    else:
        basedir = lastdir
    atual += 1
    print '  '*level, 'Entrando na pasta "%s"... (%d/%d)' % (lastdir,atual,total)
    for f in files:
        if type(f) is Directory:
            atual = renomRec(f, basedir, atual, level + 1)
            print ''
        elif sagaz and f.basename in ('Makefile','Thumbs.db'):
            # Não processa esses caras
            print '  '*level, ' "%s" não foi alterado (Modo sagaz) (%d/%d)' % (f.basename,atual,total)
        else:
            newf = f.basename.lower()
            if sagaz:
                newf = sagazReplaces(newf)
            if capitaliza:
                newf = capitalizaIsso(newf)
            atual += 1
            if newf != f.basename:
                print '  '*level, ' "%s" => "%s"? (%d/%d)' % (f.basename,newf,atual,total)
                if vcQuer():
                    # vamos alterar!
                    newf = path.join(basedir,newf)
                    rename(f.filename, newf)
                elif verbose:
                    print '  '*level, ' "%s" => "%s" não foi alterado (%d/%d)' % (f.basename,newf,atual,total)

            elif verbose:
                print '  '*level, '"%s" não foi alterada (%d/%d)' % (newf,atual,total)

    # não vamos esquecer do diretório base
    newbasedir = path.join(lastdir, files.dirname)
    if files.dirname != '.' and newbasedir != basedir:
        print '  '*level, 'Dir "%s" => "%s"? (%d/%d)' % (basedir,newbasedir,atual,total)
        if vcQuer():
            rename(basedir, newbasedir)
    elif verbose:
        print '  '*level, 'Dir "%s" não foi alterado (%d/%d)' % (newbasedir,atual,total)
    return atual + 1

def vcQuer():
    global force
    if force:
        return True
    else:
        try:
            answer = raw_input()
        except KeyboardInterrupt:
            print u"ABORTANDO (usuário apertou C^-C)"
            from sys import exit
            exit(1)

        answer = answer.lower()
        return (answer in ('', 's', 'y', 'sim', 'yes'))

def sagazReplaces(newf):
    replaces = {
        '%20' : ' ',
        '_' : ' ',
        '+' : ' ',
        '  ' : ' ',
        ' .' : '.',
        'copy of ' : '',
    }
    # abaixo é O(len(replaces)^2), eu sei...
    for tmp in range(len(replaces)):  # para que haja as transformações completas
        # por exemplo: 'a%20%20.pdf' => 'a.pdf'
        for r in replaces:
            if newf.find(r) >= 0:
                newf = newf.replace(r,replaces[r])

    pontos = newf.split('.')
    if len(pontos) > 2:  # opa! tá separando espaço por pontos?!
        newf = '%s.%s' % (' '.join(pontos[:-1]), pontos[-1])  # %s.%s => nome_do_arquivo.extensão

    return newf

def capitalizaIsso(s):
    def capitalizaPalavra(p):
        if p.startswith("(") or p.startswith("(") or p.startswith("{") or p.startswith("["):
            return p[0] + p[1:].capitalize()
        else:
            return p.capitalize()

    final = []
    for palavra in s.split(" "):
        final.append(capitalizaPalavra(palavra))
    return " ".join(final)

if __name__ == "__main__":
    from sys import argv
    from optparse import OptionParser

    usage = u"""uso: %prog [-h --help] [-v --verbose] [-s --sagaz] [DIRETORIO]
DIRETORIO padrão a ser usado será o atual"""
    parser = OptionParser(usage,
        description=renomLower.__doc__.replace('\t',''),
        version=u"%%prog %s" % __VERSION__)
    parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False, 
        help=u"Mostra informações de arquivos que não serão processados")
    parser.add_option('-s', '--sagaz', dest='sagaz', action="store_true", default=False, 
        help=u"Não possibilita alteração de alguns arquivos que devem ser maiúsculos (Makefile, Thumbs.db por ex), além de algumas substituições marotas")
    parser.add_option('-f', '--force', dest='force', action="store_true", default=False, 
        help=u"Altera todos os arquivos sem confirmação")
    parser.add_option('-c', '--capitaliza', dest='capitaliza', action="store_true", default=False, 
        help=u"Deixa a primeira letra de cada palavra maiúscula")
    (opt, args) = parser.parse_args()

    verbose = opt.verbose
    sagaz = opt.sagaz
    force = opt.force
    capitaliza = opt.capitaliza
    renomLower(args)

