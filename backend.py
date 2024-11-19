"""
Backend shiny
"""

# Bibliotecas autorais
from gerador import gerador

# Bibliotecas não autorais
from os import path
from time import time
from math import log10
from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from urllib.parse import urlencode, parse_qs

app_ui = ui.page_fluid(
    # Layout
    ui.row(
        ui.column(
            3,
            ui.input_text("input_funcao", "Função", placeholder = "a*x**2 + b*x + c"),
            ui.input_numeric("input_limite_inferior", "Limite Inferior", value = 0),
            ui.input_numeric("input_limite_superior", "Limite Superior", value = 10),
            ui.input_text("args_input", "Argumentos (separado por vírgula)", placeholder="argumento_1, argumento_2, argumento_3"),
        ),
        ui.column(
            3,
            ui.output_ui("dynamic_inputs"),
        ),
        ui.column(
            3,
            ui.output_text_verbatim("print_output"),
        ),
        ui.column(
            3,
            ui.div(
                ui.output_text_verbatim("print_readme"),
                style="height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;",
            ),
        )
    ),
    ui.output_plot("plot", width="100%", height="600px")    
)


def server(input, output, session):
    """
    Server Shiny
    """

    # Atualiza a query string sempre que um input muda
    @reactive.Effect
    @reactive.event(input.input_funcao, input.input_limite_inferior, input.input_limite_superior, input.args_input)
    def update_query_string():
        try:
            # Criar o dicionário de parâmetros
            query_params = {
                "input_funcao": input.input_funcao(),
                "limite_inferior": input.input_limite_inferior(),
                "limite_superior": input.input_limite_superior(),
                "args_input": input.args_input(),
            }
            # Obter a URL base
            current_url = session.get_url()  # Ex: http://localhost:8000/
            base_url = current_url.split("?")[0]  # Remove query string anterior, se existir

            # Atualizar a URL com os parâmetros
            new_url = f"{base_url}?{urlencode(query_params)}"
            session.redirect(new_url)  # Redireciona para a nova URL
        except Exception as e:
            print(f"Erro ao atualizar a query string: {e}")

    @reactive.Effect
    def initialize_from_query():
        try:
            # Obter a query string da URL
            current_url = session.get_url()
            query_string = current_url.split("?")[1] if "?" in current_url else ""
            query_params = parse_qs(query_string)

            if query_params:
                # Extrair os valores
                funcao = query_params.get("input_funcao", [""])[0]
                limite_inferior = float(query_params.get("limite_inferior", [0])[0])
                limite_superior = float(query_params.get("limite_superior", [10])[0])
                args_input = query_params.get("args_input", [""])[0]

                # Atualizar os inputs
                session.send_input_message("input_funcao", {"value": funcao})
                session.send_input_message("input_limite_inferior", {"value": limite_inferior})
                session.send_input_message("input_limite_superior", {"value": limite_superior})
                session.send_input_message("args_input", {"value": args_input})

        except Exception as e:
            print(f"Erro ao inicializar a partir da query string: {e}")

    # Reatividade se dará por essa função
    @reactive.Calc
    def dynamic_args():
        args = input.args_input().replace(" ","").split(",")  # Divide os argumentos
        return sorted(list(set(args)))
        
    def dynamic_boxes():
        args = dynamic_args()
        return [arg.strip() for arg in args if arg.strip()] # Remove espaços extras

    # Caixa dos argumentos
    @output
    @render.ui
    def dynamic_inputs():
        boxes = [ui.input_numeric(f"arg_{arg}", f"Argumento '{arg}'", value = 1) for i, arg in enumerate(dynamic_boxes())]
        return boxes

    # Gráfico
    @output
    @render.plot
    def plot():
        dynamic_values:list = dynamic_args()

        args:dict = {}
        for key in dynamic_values:
            args[key] = float(session.input[f"arg_{key}"]())

        try:
            funcao_usuario = gerador(funcao = input.input_funcao(), argumentos = list(args.keys()))
            
            total:float = input.input_limite_superior() - input.input_limite_inferior()
            
            tempo_medio = -time()
            funcao_usuario(x = input.input_limite_inferior(), **args)
            funcao_usuario(x = input.input_limite_superior(), **args)
            tempo_medio += time()
            n:int = min(200, max(10, int(0.1/tempo_medio)))

            x:list = [input.input_limite_inferior() + i * total / (n-1) for i in range(n)]
            
            y:list = [funcao_usuario(x = x, **args) for x in x]  # Criação de valores para o eixo y
            
        except Exception as error:
            if isinstance(error, NameError):
                updated_text:str = f"{input.args_input()}," + error.name
                session.send_input_message("args_input", {"value": updated_text})
            else:
                print(f"ERRO: {error}")
                return None
                            

        fig, ax = plt.subplots()
        ax.plot(x, y)  # Gráfico simples com os limites

        min_, max_ = min(y), max(y)
        dif_:int = 10**int(log10(max_ - min_) - 1)
        horizontal_lines = [i*dif_ for i in range(int(min_/dif_), int(max_/dif_ + 1))]
        for line in horizontal_lines:
            ax.axhline(y = line, color = 'gray', linestyle = '--', linewidth = 0.5)
            
        ax.set_title(f"Grafico da função [{input.input_limite_inferior()}, {input.input_limite_superior()}], n: {n}, dif: {dif_}")
    
        return fig

    # Infos
    @output
    @render.text
    def print_output():
        dynamic_values = [f"arg_{value}" for value in dynamic_args()]
        args:list = sorted(list(set([value.replace("arg_", "") for value in dynamic_values])))

        output_text = (
            f"Função: {input.input_funcao()}\n"
            f"Limite Superior: {input.input_limite_inferior()}\n"
            f"Limite Inferior: {input.input_limite_superior()}\n"
            f"Argumentos: {', '.join(args)}\n"
            f"Argumentos Dinâmicos: {dynamic_values}"
        )
        return output_text

    # Instruções
    @output
    @render.text
    def print_readme():
        if path.exists("README.md"):
            with open("README.md", "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "O arquivo README.md não foi encontrado."


app = App(app_ui, server)
