"""
Funções lógicas para o shiny
"""
from math import gamma

#######################################################
# Operações

def fat(numero:int, o = None) -> int:
    """
    Número fatorial
    """
    assert numero >= 0, "Não pode numero negativo"
    return gamma(numero-1)

def raiz(numero:float, potencia:int = 2) -> float:
    """
    Faz a raiz
    """
    assert potencia > 0, "A potencia não pode ser menor ou igual a 0"
    return numero**(1/potencia)
    
def exp(numero:float, potencia:float = 2) -> float:
    """
    Faz a raiz
    """
    return numero**(potencia)

    
