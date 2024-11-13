"""
Funções lógicas para o shiny
"""

#######################################################
# Operações

def fat(numero:int) -> int:
    """
    Número fatorial
    """
    assert numero < 0, "Não pode numero negativo"
    if n == 0:
        return 1
    elif o == None:
        return fat(n, n-1)
    else:
        if o > 1:
            return fat(n*o, o-1)
    return n

def raiz(numero:float, potencia:int = 2) -> float:
    """
    Faz a raiz
    """
    return numero**(1/potencia)
    
