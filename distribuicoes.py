"""
Distribuicoes
"""
from funcoes_especiais import *

def poisson(x:float, lambda_:float) -> float:
    try:
        return (2.71**(-lambda_) * lambda_**x)/fat(x)
    except:
        return 0

def normal(x:float) -> float:
    pass

def exp(x:float) -> float:
    pass

exponencial = exp

def binom(x:float) -> float:
    pass

binomial = binom
