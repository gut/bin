#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Arrancador de acentos
#Copyright  (2004) João S. O. Bueno 
#Permissao para uso e modificacao conforme a LGPL.


#uso: check_alphanum (string) retorna verdadeiro se a string é imprimivivel
#strip_diacriticals : troca todos os acentos pelos equivalentes nao acentuados.
# e retorna a string alterada

import copy

conversion= { "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
     "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
     "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u",
     "ã": "a", "õ": "o", "ñ": "n", "ç":"c",
     "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
     "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U",
     "Â": "A", "Ê": "E", "Î": "I", "Ô": "O", "Û": "U",
     "Ã": "A", "Õ": "O", "Ñ": "N", "Ç": "C",
     "Ü": "U", "û":"u", "Ä":"A", "ä":"a", "Ë":"E", "ë":"e",
     "Ï":"I", "ï":"i", "Ö":"O", "ö":"o", "ð":"?", "ß":"ss",
      "Å":"A","å":"a", "ø":"o", "Ø":"O", "Þ":"?" , "æ":"ae"
     }

alphanum_ops_CHECK=0
alphanum_ops_FIX=1

def _alphanum_util (string, operation):
    """check if all characters are in printable range
    and valid in roman alphabet languages"""
    global alphanum_ops_CHECK, alphanum_ops_FIX
    global conversion
    ok=1
    out_string=""
    skip=0
    aux=len(string)
    for i in xrange(aux):
        if skip:
            skip-=1
            continue
        char=string[i]
        num=ord(char)
        if num>=32 and num<=127:
            out_string+=char
        else:
            if num> 127 and i<aux-1 and conversion.has_key (string[i]+string[i+1]):
                out_string+=conversion[string[i]+string[i+1]]
                skip=1
            else:
                out_string+="?"
                ok=0
                if operation==alphanum_ops_CHECK:
                    return ok
                #the following values are picked from utf-8 specification
                #and mean the number of bytes following the first byte > 0xc0
                #that are part of the same utf-8 character
                if num >= 0xf0:
                    skip=3
                elif num >= 0xe0:
                    skip-2
                elif num>= 0xc0:
                    skip=1
                else:
                    skip=0
    if operation==alphanum_ops_CHECK:
        return ok
    else:
        return out_string

def check_alphanum (string):
    """check if all characters are in printable range and
    valid in romam alphabet languages"""
    global alphanum_ops_CHECK, alphanum_ops_FIX
    return _alphanum_util (string, alphanum_ops_CHECK)

def strip_diacriticals (string):
    """replace non ASCII characters  for '?' ' or equiv.
    letter if it is an western european accented letter."""
    global alphanum_ops_CHECK, alphanum_ops_FIX
    return _alphanum_util (string, alphanum_ops_FIX)

# A partir daqui foi feito por Gustavo Serra Scalet
if __name__ == "__main__":
    from sys import argv, exit
    from os import sep

    try:
        ori = argv[1]
        dest = argv[2]
    except:
        print 'Uso: %s nome_do_arquivo_origem nome_do_arquivo_destino' % (
            argv[0].split(sep)[-1],)
        exit(1)

    oriCont = open(ori,'r').read()
    # como '\n' nao é um caractere imprimivivel, retornaria '?',
    # faremos o processo por partes
    oriLinhas = oriCont.splitlines()
    destLinhas = []
    for i in oriLinhas:
        destLinhas.append(strip_diacriticals(i))
    # gravando alterações
    #print destLinhas
    destF = open(dest,'w')
    destF.write('\n'.join(destLinhas))
    destF.close()
    exit(0)
