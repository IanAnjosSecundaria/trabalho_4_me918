"""
Funções de geração de função
"""

# Bibliotecas autorais
from funcoes_especiais import *
from distribuicoes import *

# Bibliotecas não autorais
from random import random
from math import log10, log2, log


def gerador(funcao:str, argumentos:list = []) -> "lambda":
    """
    Gera a função específica do usuário
    """
    
    argumentos:set = sorted(list(set(argumentos)))
    if "x" in argumentos:
        argumentos.pop("x")

    temporario:str = f"lambda x, {', '.join(argumentos)} : {funcao}"

    return eval(temporario)
