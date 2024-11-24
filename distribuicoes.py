"""
Distribuicoes
"""
from funcoes_especiais import *
from time import sleep
from math import sqrt

DISTRIBUICOES = ["a*x**2 + b*x + c",
                 "exp(x, lambda_)",
                 "poisson(x, lambda_)",
                 "normal(x, sigma, mi)",
                 "binomial(x, n, p)"]

def poisson(x:float, lambda_:float) -> float:
    try:
        return (2.7182**(-lambda_) * lambda_**x)/fat(x)
    except:
        return 0

def normal(x:float, sigma:float, mi:float) -> float:
    if sigma <= 0:
        return 0
    return (1/(sigma*sqrt(2 * 3.1415)) * 2.7182**(-0.5 * ((x-mi)/sigma)**2))

def exp(x:float, lambda_:float) -> float:
    try:
        if x >= 0:
            return  (lambda_*2.7182**(-lambda_*x))
        else:
            return 0
    except:
        return 0 

exponencial = exp

def binom(x:float, n:int, p:float) -> float:
    try:
        if x == n == 0:
            return 1
        if n > 0 and 0 <= p <= 1:
            return  (fat(n)/(fat(x)*fat(n-x)))* p**x * (1-p)**(n-x)
        else:
            return 0
    except:
        return 0

binomial = binom
