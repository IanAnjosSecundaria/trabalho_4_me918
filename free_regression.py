from inspect import signature # Para pegar os argumentos de uma função
from copy import deepcopy
from random import random, seed

def least_squares(vector_1:list, vector_2:list) -> float:
    """
    Função de minimos quadrados
    """
    return sum([(vector_1[i] - vector_2[i])*(vector_1[i] - vector_2[i]) for i in range(len(vector_1))])

class Regression:
    """
    Classe de regressão que aceita qualquer função como regressora.

    Metodo:
        Acha aleatóriamente os parâmetros da função de regressão passada usando algum tipo de função de perda.
        1. Começa com os parâmetros modificaveis sendo igual a 1;
        2. Altera esses parâmetros em -<precision>/2 até <precision>/2 para cima ou para baixo;
        3. Se precision <presision> minima definida pelo usuário ele passa para o passo 5;
        4. Se ele não melhora em <iterations> iterações, ele divide precision por 2 e volta para o passo (2);
        5. Salva o erro e os parâmetros ótimos que podem ser acessados pelo usuário. 

    Args:
        function (function): A função qual o usuário quer fazer a regressão, essa função deve sempre ter a variável regressora chamada de x.
        regressors (list): Lista de regressores, não é precisso passar se a função tiver apenas um parâmetro regressor e ele se chame 'x'.
        loss_function (function): Função de perda, é a função 'least squares' mas pode ser qualquer uma passada pelo usuário.
    """
    __slots__ = ("iterations", "params", "regressors", "__function", "__args_function", "__seed", "__lock", "__loss_function", "__error")
    
    def __init__(self, function:"function", regressors:list = None, loss_function:"function" = least_squares) -> None:
        """
        Inicializa a classe.
        """
        assert callable(function), f"<function> is a {type(function)} not a function"
        assert callable(loss_function), f"<loss_function> is a {type(loss_function)} not a function"
        
        self.__function:"function" = function
        self.__loss_function:"function" = loss_function
        self.__error:float = None
        
        temp = tuple(signature(function).parameters.keys())
        assert len(temp) >= 2, "Your function must have at least two parameters. Example f(x, b) = x*b = y"

        # Definindo regressora
        if regressors == None:
            assert "x" in temp, "The passed function must have the parameter 'x' or explicitly specify the regressors with the parameter 'regressors'"
            self.regressors = ["x"]
        elif type(regressors) == int or type(regressors) == float:
            self.regressors = [regressors]
        else:
            self.regressors = regressors

        # Argumentos da função
        self.__args_function:dict = {}
        self.params:list = []
        for parameter in temp:
            if parameter not in self.regressors:
                self.params.append(parameter)
                self.__args_function[parameter] = 0.1
        
        self.__seed = None
        self.iterations:int = min(50 * len(self.__args_function.keys()), 500) # Quanto mais parâmetros mais iterações eu precisso para que o valor mude

        # Variáveis bloqueadas
        self.__lock = {}

    def __eq__(self, obj) -> bool:
        """
        Confere se as funções de regressões são as mesmas.
        """
        assert type(obj) == Regression, "Only Regression objects can be compared"
        return True if self.__function == obj.__function else False

    def __repr__(self) -> str:
        """
        Mostra os argumentos da classe.
        """
        output:str = f"FUNCTION: {self.__function.__name__}"
        if self.__error != None:
            output += f"\nLOSS FUNCTION({self.__loss_function.__name__}): {self.__error:0.08f}"
        output += f"\nREGRESSORS: {', '.join(self.regressors)}"
        if len(self.__lock) > 0:
            output += f"\nLOCK PARAMS: {', '.join(self.__lock)}"
        output += "\nPARAMS:"
        for arg in self.__args_function.keys():
            output += f"\n  {arg} = {self.__args_function[arg]:0.08f}"
        return output

    def __len__(self) -> list:
        """
        Retorna a dimensão sendo:
            dim_regressorses
        """
        return len(self.regressors)

    def __getitem__(self, index:str) -> float:
        """
        Mostra o argumento especifico pedido.
        """
        assert type(index) == str, "The index must be a character(chr)"
        assert index in self.params, f"The index '{index}' must exist in params '{', '.join(self.params)}'"
        return self.__args_function[index]

    def __setitem__(self, index:str, value:float) -> float:
        """
        Inicia um valor em um ponto especifico.
        """
        assert type(index) == str, "The index must be a character(chr)"
        assert index in self.params, f"The index '{index}' must exist in params '{', '.join(self.params)}'"
        assert type(value) == int or type(value) == float, f"<value> must to be a int or float not a {type(value)}"
        self.change(**{index:value})

    def __add__(self, obj) -> "Regression":
        """
        + para mistura.
        self + obj
        """
        modified_class = eval(self.__generic_function(obj, operator = "+"))
        if type(self) == type(obj):
            modified_class.__function.__name__ = f"{self.__function.__name__}_add_{obj.__function.__name__}"
        else:
            modified_class.__function.__name__ = f"{self.__function.__name__}_add_number"
        return modified_class

    def __sub__(self, obj) -> "Regression":
        """
        - para mistura.
        self - obj
        """
        modified_class = eval(self.__generic_function(obj, operator = "-"))
        if type(self) == type(obj):
            modified_class.__function.__name__ = f"{self.__function.__name__}_sub_{obj.__function.__name__}"
        else:
            modified_class.__function.__name__ = f"{self.__function.__name__}_sub_number"
        return modified_class

    def  __mul__(self, obj) -> "Regression":
        """
        * para mistura.
        self * obj
        """
        modified_class = eval(self.__generic_function(obj, operator = "*"))
        if type(self) == type(obj):
            modified_class.__function.__name__ = f"{self.__function.__name__}_mul_{obj.__function.__name__}"
        else:
            modified_class.__function.__name__ = f"{self.__function.__name__}_mul_number"
        return modified_class

    def __truediv__(self, obj) -> "Regression":
        """
        / para mistura.
        self / obj
        """
        modified_class = eval(self.__generic_function(obj, operator = "/"))
        if type(self) == type(obj):
            modified_class.__function.__name__ = f"{self.__function.__name__}_truediv_{obj.__function.__name__}"
        else:
            modified_class.__function.__name__ = f"{self.__function.__name__}_truediv_number"
        return modified_class

    def __pow__(self, obj) -> "Regression":
        """
        ** para mistura.
        self ** obj
        """
        modified_class = eval(self.__generic_function(obj, operator = "**"))
        if type(self) == type(obj):
            modified_class.__function.__name__ = f"{self.__function.__name__}_pow_{obj.__function.__name__}"
        else:
            modified_class.__function.__name__ = f"{self.__function.__name__}_pow_number"
        return modified_class

    def __rshift__(self, obj) -> None:
        """
        Passa os parâmetros de:
        self para obj
        """
        assert type(obj) == Regression, "This operation only allows another instance of the Regression class"
        for arg in self.__args_function.keys():
            if arg in obj.__args_function.keys():
                obj.__args_function[arg] = self.__args_function[arg]

    def __lshift__(self, obj) -> None:
        """
        Passa os parâmetros de:
        obj para self
        """
        obj.__rshift__(self)

    def save(self, name:str) -> bool:
        """
        Salva os argumentos de memória em um arquivo chamado <name>.memory
        """
        with open(f"{name.replace('.memory', '')}.memory", "w") as arq:
            arq.write(f"{self.__args_function}")

    def open(self, name:str) -> bool:
        """
        Abre os argumentos de memória em um arquivo chamado <name>.memory
        """
        with open(f"{name.replace('.memory', '')}.memory", "r") as arq:
            self.__args_function = eval(arq.read())

    def loss_function(self, function:"function") -> None:
        """
        Muda a função de perda usada para a regressão.
        """
        self.__loss_function:"function" = function

    def operation(self, obj, operator:str) -> "Regression":
        """
        <operator> para mistura.
        self <operador> obj
        """
        modified_class = eval(self.__generic_function(obj, operator = operator))
        if type(self) == type(obj):
            modified_class.__function.__name__ = f"{self.__function.__name__}_generic_{obj.__function.__name__}"
        else:
            modified_class.__function.__name__ = f"{self.__function.__name__}_generic_number"
        return modified_class


    def __generic_function(self, obj:"Regression", operator:str) -> str:
        """
        Cria a função genérica e deixa como variável global as funções necessárias.
        """

        if type(obj) == int or type(obj) == float:
            globals()[f"{self.__function.__name__}"] = self.__function
            
            all_parameters = list(set(self.regressors) | set(self.params))
            all_regressorss = list(self.regressors)
            
            inputs_1 = ""
            for input_ in list(set(self.regressors) | set(self.params)):
                inputs_1 += f"{input_} = {input_},"            
            return f"Regression(lambda {', '.join(all_parameters)} : {self.__function.__name__}({inputs_1}) {operator} {obj}, regressors = {all_regressorss})"

        else:
            assert type(obj) == type(self), f"{obj} must be of type class 'Regression'"
            
            globals()[f"{self.__function.__name__}"] = self.__function
            globals()[f"{obj.__function.__name__}"] = obj.__function
            
            all_parameters = list(set(self.regressors) | set(obj.regressors) | set(self.params) | set(obj.params))
            all_regressorss = list(set(self.regressors) | set(obj.regressors))
            
            inputs_1 = ""
            for input_ in list(set(self.regressors) | set(self.params)):
                inputs_1 += f"{input_} = {input_},"

            inputs_2 = ""
            for input_ in list(set(obj.regressors) | set(obj.params)):
                inputs_2 += f"{input_} = {input_},"
            
            return f"Regression(lambda {', '.join(all_parameters)} : {self.__function.__name__}({inputs_1}) {operator} {obj.__function.__name__}({inputs_2}), regressors = {all_regressorss})"

    def set_seed(self, seed:int) -> None:
        """
        Coloca uma seed.
        """
        assert type(seed) == int, "The seed must be an integer(int)!"
        self.__seed = seed

    def lock(self, **args) -> None:
        """
        Atualiza as variáveis que devem estar travadas.
        """
        for arg in args:
            assert arg in self.__args_function.keys(), f"'{arg}' not in parameters of the function {self.__function.__name__}"
            self.__lock[arg] = args[arg]

    def change(self, **args) -> None:
        """
        Troca um valor para que o chute inicial dele seja diferente.
        """
        for arg in args:
            assert arg in self.__args_function.keys(), f"'{arg}' not in parameters of the function {self.__function.__name__}"
            self.__args_function[arg] = args[arg]

    def change_all(self, value:float) -> None:
        """
        Troca todos os valores para que o chute inicial dele seja diferente.
        """
        assert type(value) == int or type(value) == float or type(value) == list or type(value) == tuple, f"<value> must to be a float or int not {type(value)}"

        if type(value) == list or type(value) == tuple:
            assert len(value) == 2, f"If <value> has to be 2 values, [min, max]"

            if self.__seed is not None:
                seed(self.__seed)
            
            for arg in self.__args_function.keys():
                self.__args_function[arg] = random()*(max(value) - min(value)) - min(value)

        else:
            for arg in self.__args_function.keys():
                    self.__args_function[arg] = value

    def prediction(self, list_prediction:list = None, **x_args) -> float:
        """
        Faz a previsão de f(...) = y.

        Args:
            list_prediction (list): É uma lista de listas, faz a predição com esses valores.
            x_args (**dict): Faz a predição de acordo com os valores pedidos.

        Returns:
            float: Valor predito.
        """

        if type(list_prediction) == list or type(list_prediction) == tuple: # Caso o usuário tenha passado uma série de valores para a predição
            assert type(list_prediction[0]) == list or type(list_prediction[0]) == tuple, "If you want to pass a series of values​to predict, you should pass the list of lists of values with the regressors parameters"
            assert min(map(len, list_prediction)) == max(map(len, list_prediction)) == len(self.regressors), f"Your list of lists must be {len(list_prediction)} by {len(self.regressors)} in size"

            results = []
            x_args = {}
            for values in list_prediction:
                for i in range(len(self.regressors)):
                    x_args[self.regressors[i]] = values[i]
                results.append(self.__function(**x_args, **self.__args_function))
                
            return results
        
        else: # Caso o usuário tenha passado valores específicos para a predição
            assert len(set(x_args.keys()) & set(self.__args_function.keys())) == 0, f"You cannot pass a parameter as a regressors that is already being used as a prediction parameter.\n  regressors parameters: {', '.join(x_args.keys())}\n  Predictor parameters: {', '.join(self.__args_function.keys())}"
            assert set(x_args.keys()) == set(self.regressors), f"Pass regressors parameters correctly\n  regressors parameters passed: {', '.join(x_args.keys())}\n  Expected regressors parameters: {', '.join(self.regressors)}"

            return self.__function(**x_args, **self.__args_function)

    def run(self, data:[list], precision:float = 0.001, booster:float = 100) -> None:
        """
        Faz a regressão.

        Args:
            data(list(list)): lista de listas com x e y.
            precision(float): Numero da precisão para achar os parâmetros esperados.
        """

        assert type(data) == list, f"The data must be a list of lists not {type(data)}"
        assert type(data[0]) == list, f"The data must be a list of lists not {type(data[0])}"
        assert len(data[0]) == len(self.regressors) + 1, f"The list of lists must have an x_n and a y parameter, for example [[x_0, x_1, ..., y], [x_0, x_1, ..., y], ...]\n\tSize of the passed list: {len(data[0])}\n\tExpected size: {len(self.regressors) + 1}"
        assert (k := list(map(len, data))) and max(k) == min(k), "The data list must be the same size in all itens"
        assert type(precision) == int or type(precision) == float, "Precision has to be a float or int"

        # Iniciando a seed
        if self.__seed is not None:
            seed(self.__seed)

        # Pegando y esperado
        y_expected = [data[i][-1] for i in range(len(data))]

        # Salvando argumentos iniciais para a função
        args_temp:dict = {}
        for parameter in self.__args_function.keys():
            if parameter not in self.__lock.keys():
                args_temp[parameter] = self.__args_function[parameter]
            else:
                args_temp[parameter] = self.__lock[parameter] # Caso a variável deva estar travada

        precision_final, precision = precision/2, precision * booster
        while precision >= precision_final: # Vai diminuindo a variação da busca
            with_no_iteration = 0
            while with_no_iteration < self.iterations:
                with_no_iteration += 1
                
                # y predito
                y_predicted:list = []
                for *x, _ in data:

                    # Separando as variáveis regressoras
                    x_args:dict = {}
                    for i in range(len(x)):
                        x_args[self.regressors[i]] = x[i]

                    # Fazendo a predição
                    y_predicted.append(self.__function(**x_args, **args_temp))

                # Resultado dos minimos quadrados
                result = self.__loss_function(y_predicted, y_expected)

                # Atualizando melhores parâmetros para regressora
                if not "best_result" in locals():
                    best_result:float = result
                    best_args = deepcopy(args_temp)

                if result < best_result:
                    with_no_iteration = 0
                    best_result:float = result
                    best_args = deepcopy(args_temp)
                else:
                    args_temp = deepcopy(best_args)

                for parameter in self.__args_function.keys():
                    if parameter not in self.__lock.keys():
                        args_temp[parameter] += random()*precision - precision/2
                        
            # Aumenta a precisão
            precision /= 2

        # Salva o resultado
        self.__args_function = best_args
        self.__error = best_result/len(data)


    def __animation_run(self, data:[list], precision:float = 0.001, booster:float = 100) -> None:
        """
        Função modificada para fazer animações.
        
        Faz a regressão.

        Args:
            data(list(list)): lista de listas com x e y.
            precision(float): Numero da precisão para achar os parâmetros esperados.
        """
        from make_animation import plot_expected_and_save

        assert type(data) == list, f"The data must be a list of lists not {type(data)}"
        assert type(data[0]) == list, f"The data must be a list of lists not {type(data[0])}"
        assert len(data[0]) == len(self.regressors) + 1, f"The list of lists must have an x_n and a y parameter, for example [[x_0, x_1, ..., y], [x_0, x_1, ..., y], ...]\n\tSize of the passed list: {len(data[0])}\n\tExpected size: {len(self.regressors) + 1}"
        assert (k := list(map(len, data))) and max(k) == min(k), "The data list must be the same size in all itens"
        assert type(precision) == int or type(precision) == float, "Precision has to be a float or int"

        # Iniciando a seed
        if self.__seed is not None:
            seed(self.__seed)

        # Pegando y esperado
        y_expected = [data[i][-1] for i in range(len(data))]

        # Salvando argumentos iniciais para a função
        args_temp:dict = {}
        for parameter in self.__args_function.keys():
            if parameter not in self.__lock.keys():
                args_temp[parameter] = self.__args_function[parameter]
            else:
                args_temp[parameter] = self.__lock[parameter] # Caso a variável deva estar travada

        iteration_:int = 0
        qnt_:int = 0
        qnt_plot:list = [int(i + 1.04**i) for i in range(5_000)]
        precision_final, precision = precision/2, precision * booster
        while precision >= precision_final: # Vai diminuindo a variação da busca
            with_no_iteration = 0
            while with_no_iteration < self.iterations:
                iteration_ += 1
                with_no_iteration += 1
                
                # y predito
                y_predicted:list = []
                for *x, _ in data:

                    # Separando as variáveis regressoras
                    x_args:dict = {}
                    for i in range(len(x)):
                        x_args[self.regressors[i]] = x[i]

                    # Fazendo a predição
                    y_predicted.append(self.__function(**x_args, **args_temp))

                # Resultado dos minimos quadrados
                result = self.__loss_function(y_predicted, y_expected)

                # Atualizando melhores parâmetros para regressora
                if not "best_result" in locals():
                    best_result:float = result
                    best_args = deepcopy(args_temp)
                    self.__args_function = best_args
                    plot_expected_and_save(self, data, name = f"img_{int(iteration_):04.00f}")
                    qnt_ += 1

                if result < best_result:
                    with_no_iteration = 0
                    best_result:float = result
                    best_args = deepcopy(args_temp)
                    self.__args_function = best_args
                    if qnt_ in qnt_plot:
                        plot_expected_and_save(self, data, name = f"img_{int(iteration_):04.00f}")
                    qnt_ += 1
                    
                else:
                    args_temp = deepcopy(best_args)

                for parameter in self.__args_function.keys():
                    if parameter not in self.__lock.keys():
                        args_temp[parameter] += random()*precision - precision/2
                        
            # Aumenta a precisão
            precision /= 2

        # Salva o resultado
        self.__args_function = best_args
        self.__error = best_result/len(data)
