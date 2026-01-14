import dash
from dash import dcc, html
from matplotlib.dates import date2num, num2date
import webbrowser




class GraficoInteractivo():
    def __init__(self,df):
        self.df = df.copy()
        self.x = date2num(self.df["tspan"])
        self.cols = [col for col in df.columns if col != "tspan"]
        self.data = []

    def __create_data(self):
        for col in self.cols:
            d = {
                "x": self.x,
                "y": self.df[col],
                "type": 'scatter',
                "name": col
            }
            self.data.append(d)
            
    def start_app(self):
        # Llenar la lista de datos antes de crear el layout
        self.__create_data()
        app = dash.Dash(__name__)
        app.layout = html.Div(
            children=[
                html.H1(children="Fer"),
                html.Div(children="Subtítulo"),
                dcc.Graph(
                    id="grafico1",
                    figure={
                        "data": self.data,
                        "layout": {'title': 'Visualización con Dash'}
                    }
                )
            ]
        )

        # Abrir navegador automáticamente
        webbrowser.open_new("http://127.0.0.1:8050/")

        app.run_server(debug=True)
        
        