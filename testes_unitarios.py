import unittest
from distribuicoes import poisson, normal, exp, binomial
from funcoes_especiais import fat
import math


class TestDistribuicoes(unittest.TestCase):

    def test_poisson(self):
        # Teste básico para a função de distribuição Poisson
        resultado = poisson(2, 3)
        self.assertAlmostEqual(resultado, 0.2241, places=4)  # Valor esperado

        # Teste para valores fora do domínio (x negativo)
        resultado_invalido = poisson(-1, 3)
        self.assertEqual(resultado_invalido, 0)

        # Teste com lambda = 0 (deve retornar 0, pois qualquer número elevado a qualquer coisa com lambda 0 é 1, mas multiplicado por e^-lambda dá 0)
        resultado_lambda_zero = poisson(2, 0)
        self.assertEqual(resultado_lambda_zero, 0)

        # Teste com um valor muito grande para x e lambda
        resultado_grande = poisson(100, 100)
        self.assertGreater(resultado_grande, 0)

    def test_normal(self):
        # Teste básico para a função de distribuição normal
        resultado = normal(0, 1, 0)
        self.assertAlmostEqual(resultado, 0.3989, places=4)  # Normal padrão

        # Teste com valor fora do domínio (sigma negativo)
        resultado_invalido = normal(0, -1, 0)
        self.assertGreater(resultado_invalido, 0)  # A distribuição não deve ser negativa

        # Teste com valor extremo para a normal (pode se aproximar de zero, mas não será zero exato)
        resultado_extremo = normal(100, 10, 0)
        self.assertAlmostEqual(resultado_extremo, 0.0, places=4)

        # Teste para valores grandes de sigma e mi
        resultado_grande_sigma = normal(0, 1000, 0)
        self.assertAlmostEqual(resultado_grande_sigma, 0.0, places=4)

    def test_exp(self):
        # Teste básico para a função exponencial
        resultado = exp(1, 1)
        self.assertAlmostEqual(resultado, 0.3679, places=4)

        # Teste com valores negativos para x (deve retornar 0)
        resultado_negativo = exp(-1, 1)
        self.assertEqual(resultado_negativo, 0)

        # Teste com lambda muito grande (deve retornar um valor pequeno)
        resultado_lambda_grande = exp(1, 100)
        self.assertAlmostEqual(resultado_lambda_grande, 0, places=5)  # Deveria ser muito pequeno

        # Teste com lambda pequeno
        resultado_lambda_pequeno = exp(1, 0.1)
        self.assertAlmostEqual(resultado_lambda_pequeno, 0.9048, places=4)

    def test_binomial(self):
        # Teste básico para a função binomial
        resultado = binomial(2, 5, 0.5)
        self.assertAlmostEqual(resultado, 0.3125, places=4)

        # Teste para x > n (deve retornar 0)
        resultado_invalido = binomial(6, 5, 0.5)
        self.assertEqual(resultado_invalido, 0)

        # Teste para p = 0 (probabilidade de sucesso é 0)
        resultado_p_zero = binomial(2, 5, 0)
        self.assertEqual(resultado_p_zero, 0)

        # Teste para p = 1 (probabilidade de sucesso é 1)
        resultado_p_um = binomial(5, 5, 1)
        self.assertEqual(resultado_p_um, 1)

        # Teste para n = 0 (não há tentativas)
        resultado_n_zero = binomial(0, 0, 0.5)
        self.assertEqual(resultado_n_zero, 1)

    def test_fatorial(self):
        # Teste para a função de fatorial
        resultado = fat(5)
        self.assertEqual(resultado, 120)

        # Teste para fatorial de 0 (deve retornar 1)
        resultado_zero = fat(0)
        self.assertEqual(resultado_zero, 1)

        # Teste para fatorial de um número negativo (espera-se erro)
        with self.assertRaises(AssertionError):
            fat(-5)

    def test_limites(self):
        # Teste de limites para valores extremos em algumas distribuições

        # Poisson com valores muito grandes de x e lambda
        resultado_poisson_extremo = poisson(1000, 1000)
        self.assertGreater(resultado_poisson_extremo, 0)

        # Normal com grandes valores para x
        resultado_normal_extremo = normal(1000, 10, 0)
        self.assertAlmostEqual(resultado_normal_extremo, 0.0, places=4)

        # Exponencial com lambda muito grande
        resultado_exp_extremo = exp(10, 1000)
        self.assertAlmostEqual(resultado_exp_extremo, 0.0, places=4)

        # Binomial com n muito grande e p pequeno
        resultado_binomial_extremo = binomial(500, 1000, 0.01)
        self.assertGreater(resultado_binomial_extremo, 0)

    def test_precision(self):
        # Teste para precisão dos cálculos (valores calculados manualmente ou usando uma referência)

        # Poisson para x = 2, lambda = 3
        resultado_poisson = poisson(2, 3)
        self.assertAlmostEqual(resultado_poisson, 0.2241, places=4)

        # Normal para x = 0, sigma = 1, mi = 0
        resultado_normal = normal(0, 1, 0)
        self.assertAlmostEqual(resultado_normal, 0.3989, places=4)

        # Exponencial para x = 1, lambda = 1
        resultado_exp = exp(1, 1)
        self.assertAlmostEqual(resultado_exp, 0.3679, places=4)

        # Binomial para n = 5, x = 2, p = 0.5
        resultado_binomial = binomial(2, 5, 0.5)
        self.assertAlmostEqual(resultado_binomial, 0.3125, places=4)


if __name__ == '__main__':
    unittest.main()
