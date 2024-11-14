"""
Funções de geração de função
"""
from funcoes_especiais import *

def gerador(funcao:str, argumentos:list = []) -> "lambda":
    """
    Gera a função específica do usuário
    """
    
    argumentos:set = sorted(list(set(argumentos)))
    if "x" in argumentos:
        argumentos.pop("x")

    temporario:str = f"lambda x, {', '.join(argumentos)} : {funcao}"

    return eval(temporario)
