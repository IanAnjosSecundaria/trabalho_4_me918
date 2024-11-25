# Trabalho 4 - ME918

Este projeto foi desenvolvido com o objetivo de criar uma aplicação interativa que permite a manipulação de funções matemáticas, distribuições de probabilidade, criação de funções personalizadas e interação com dados carregados ou gerados pelo usuário. Ele também oferece funcionalidades para análise de resultados e ajustes de parâmetros personalizados. A aplicação inclui recursos como definição de limites inferiores e superiores, manipulação de parâmetros e suporte à criação de novas funções.

---

## Como configurar o ambiente

Primeiramente, é necessário instalar as dependências no ambiente virtual (*venv*).

### No Linux

Na pasta `trabalho_4_me918/ambiente_virtual_venv`, execute os seguintes comandos:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r bibliotecas.txt
```

### Para rodar a aplicação

Use o comando abaixo:

```
shiny run backend.py
```

## Funcionalidades

### Botões

- Limite inferior: Permite definir o valor mínimo para a variável de entrada na função.

- Limite superior: Define o valor máximo para a variável de entrada.

- Função: Campo onde o usuário pode selecionar ou especificar a função a ser manipulada.

- Parâmetros: Permite ajustar os parâmetros das funções carregadas ou criadas.


### Funções prontas

- Função Quadrática:

```
"a*x**2 + b*x + c"
```

Realiza o cálculo de uma função polinomial de segundo grau.

- Distribuição Exponencial, exp:

```
exp(x, lambda_)
```

Retorna 0 se 𝑥 < 0 ou 𝜆≤ 0.

- Distribuição de Poisson, poisson:

```
poisson(x, lambda_)
```

Retorna 0 se houver erro nos parâmetros.

- Distribuição Normal, normal:

```
normal(x, sigma, mi)
```

Retorna 0 se \sigma ≤ 0

- Distribuição Binomial, binom:

```
binom(x, n, p)
```

Retorna 0 para n < 0 ou p fora do intervalo [0, 1]

### Criação de funções

O sistema permite que o usuário crie funções personalizadas seguindo o padrão abaixo:

- Utilize palavras reservadas como x, y e operadores matemáticos padrão (```+```, ```-```, ```*```, ```/```, ```^```).

- Insira as expressões diretamente no campo designado para novas funções.

Exemplo, para criar a função:

```
g(x)=3𝑥+5
g(x)=3x+5, insira 3*x + 5.
```

### Download e upload da memória

A aplicação permite o compartilhamento de funções, limites e parâmetros:

1. Clique no botão Download para salvar a configuração atual em um arquivo.

2. Envie o arquivo para outra pessoa.

3. A outra pessoa pode fazer o Upload do arquivo para carregar os mesmos valores na aplicação.


## Erros conhecidos

### Erro de divisão por zero

Erro de divisão por zero: Pode ocorrer se os parâmetros inseridos resultarem em divisões inválidas (ex.: \sigma = 0 na função normal).

### Erro por falta de argumentos

Ocorre quando os argumentos necessários para calcular as funções não são fornecidos.

