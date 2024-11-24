"""
Backend shiny
"""

# Bibliotecas autorais
from gerador import gerador
from distribuicoes import DISTRIBUICOES

# Bibliotecas não autorais
import asyncio
from os import path
from time import time
from math import log10
from shiny import App, ui, render, reactive, Inputs, Outputs, Session
from shiny.types import FileInfo
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from urllib.parse import urlencode, parse_qs

# Adicionar o script ao <head>
head_content = ui.tags.head(
    ui.tags.title("trabalho_4_me918"),
)

app_ui = ui.page_fluid(
    # Layout
    ui.row(
        ui.column(
            3,
            ui.input_selectize(
                "input_funcao",
                "Função",
                choices = DISTRIBUICOES,  # Opções pré-definidas
                #selected = "a*x**2 + b*x + c",  # Seleção inicial
                multiple = False,
                options = ({
                    "placeholder": "Enter text",
                    "render": ui.js_eval(
                        '{option: function(item, escape) {return "<div><strong>Select " + escape(item.label) + "</strong></div>";}}'),
                    "create": True,
                    }
                ),
            ),
            ui.input_numeric("input_limite_inferior", "Limite Inferior", value = 0),
            ui.input_numeric("input_limite_superior", "Limite Superior", value = 10),
            ui.input_text("args_input", "Argumentos (separado por vírgula)", placeholder="argumento_1, argumento_2, argumento_3"),
            ui.input_file("upload_txt", "Carregar arquivo .txt", multiple = False, accept = [".txt"]),
            ui.download_button("download_txt", "Baixar arquivo .txt"),
            ui.output_text("file_content"),
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
            total_area:float = sum(y) * (input.input_limite_superior() - input.input_limite_inferior())/n
            
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
            
        ax.set_title(f"Grafico da função [{input.input_limite_inferior()}, {input.input_limite_superior()}], Amostras: {n}, dif: {dif_}, Área: {int(total_area+0.05):0.02f}")
    
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
            #f"Argumentos Dinâmicos: {dynamic_values}"
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


    # Download
    @render.download(
        filename = lambda: f"requisicao_atual.txt"
    )
    async def download_txt():
        await asyncio.sleep(0.25)
        yield input.input_funcao() + "\n"
        yield str(input.input_limite_inferior()) + "\n"
        yield str(input.input_limite_superior()) + "\n"
        yield input.args_input() + "\n"

    # Upload
    @reactive.calc
    def parsed_file():
        file = input.upload_txt()
        if file is None:
            return None
        file_info = file[0]  # Primeiro arquivo, já que `multiple=False`
        try:
            with open(file_info["datapath"], "r", encoding="utf-8") as f:
                content = f.read()
            return content.split("\n")
        except Exception as e:
            return f"Erro ao ler o arquivo: {e}"

    @output
    @render.text
    def file_content():
        content = parsed_file()
        session.send_input_message("input_funcao", {"value": content[0]})
        session.send_input_message("input_limite_inferior", {"value": content[1]})
        session.send_input_message("input_limite_superior", {"value": content[2]})
        session.send_input_message("args_input", {"value": content[3]})
        return content if content else "Nenhum arquivo carregado."


app = App(app_ui, server)
