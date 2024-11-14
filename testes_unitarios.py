"""
Testes unitarios
"""

if __name__ == "__main__":
    from gerador import *

    funcao = "a*x**2 + b*x + c"
    funcao_temporaria = gerador(funcao = funcao, argumentos = ["a", "b", "c"])
    print(f"Printando resposta da funcao temporaria -> {funcao}\n")
    for a in range(1, 3):
        for b in range(1, 3):
            for x in range(5):
                print(f"\tx = {x}, a = {a}, b = {b}, c = 1 -> {funcao_temporaria(x = x, a = a, b = b, c = 1)}")
            print()

    funcao = "fat(x) - fat(x-1)"
    funcao_temporaria = gerador(funcao = funcao)
    print(f"\nPrintando resposta da funcao temporaria -> {funcao}\n")
    for x in range(3, 8):
        print(f"\tx = {x} -> {funcao_temporaria(x = x)}")    
