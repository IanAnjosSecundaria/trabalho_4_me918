"""
Backend shiny
"""

from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app_ui = ui.page_fluid(
    # Layout principal com as caixas de entrada fixas
    ui.row(
        ui.column(
            3,
            ui.input_text("input_funcao", "Função"),
            ui.input_numeric("input_limite_inferior", "Limite Inferior", value = 0),
            ui.input_numeric("input_limite_superior", "Limite Superior", value = 10),
            ui.input_text("args_input", "Argumentos (separado por vírgula)", placeholder="argumento_1, argumento_2, argumento_3"),
        ),
        ui.column(
            3,
            ui.output_ui("dynamic_inputs"),  # Local onde as caixas dinâmicas aparecerão
        ),
        ui.column(
            6,
            ui.output_plot("plot"),  # Espaço para o gráfico do Matplotlib
        )
    ),
    ui.output_text_verbatim("print_output")  # Área para o print dos valores
)


def server(input, output, session):
    # Reativo para gerar caixas de entrada dinâmicas com base nos argumentos
    @reactive.Calc
    def dynamic_boxes():
        args = input.args_input().split(",")  # Divide os argumentos
        return [arg.strip() for arg in args if arg.strip()]  # Remove espaços extras

    # Renderiza dinamicamente as caixas de entrada com base nos argumentos
    @output
    @render.ui
    def dynamic_inputs():
        boxes = [ui.input_numeric(f"arg_{i}", f"Argumento '{arg}'", value="") for i, arg in enumerate(dynamic_boxes())]
        return boxes

    # Cria e renderiza o gráfico usando Matplotlib
    @output
    @render.plot
    def plot():
        fig, ax = plt.subplots()
        ax.plot([input.input_limite_inferior(), input.input_limite_superior()])  # Gráfico simples com os limites
        ax.set_title(f"Grafico da função: {input.input_limite_inferior()} to {input.input_limite_superior()}")
        return fig

    # Mostra no console as respostas de cada caixa
    @output
    @render.text
    def print_output():
        #dynamic_values = [session.input(f"arg_{i}") for i in range(len(dynamic_boxes()))]
        output_text = (
            f"Função: {input.input_funcao()}\n"
            f"Limite Superior: {input.input_limite_inferior()}\n"
            f"Limite Inferior: {input.input_limite_superior()}\n"
            f"Argumentos: {input.args_input()}\n"
            #f"Argumentos Dinâmicos: {dynamic_values}"
        )
        return output_text


app = App(app_ui, server)
