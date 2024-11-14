"""
Funções lógicas para o shiny
"""

#######################################################
# Operações

def fat(numero:int, o = None) -> int:
    """
    Número fatorial
    """
    assert numero > 0, "Não pode numero negativo"
    if numero == 0:
        return 1
    elif o == None:
        return fat(numero, numero-1)
    else:
        if o > 1:
            return fat(numero*o, o-1)
    return numero

def raiz(numero:float, potencia:int = 2) -> float:
    """
    Faz a raiz
    """
    assert potencia > 0, "A potencia não pode ser menor ou igual a 0"
    return numero**(1/potencia)
    
