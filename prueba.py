import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar backend no-interactivo antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import RectangleSelector
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import ttk
import numpy as np
from datetime import datetime, timedelta
from matplotlib.figure import Figure


class InteractivePlotterTk:
    def __init__(self, data):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.data = data

        # Backup de los datos originales
        self.data_backup = data.copy()

        self.tspan_var_name = "tspan"
        self.data[self.tspan_var_name] = mdates.date2num(self.data[self.tspan_var_name])
        self.tspan = self.data[self.tspan_var_name]
        
        # Memoria de curvas que se grafican
        self.selected_columns = [] # Para guardar las columnas seleccionadas
        
        # Memoria de curvas y puntos seleccionados
        self.create_selected_points() # Es un diccionario con keys = keys del df de entrada (data). Acá se guardan los ptos seleccionados en el gráfico
        
        # Crear la interfaz
        self.create_main_frame()

        # Crear de eliminaciones
        self.create_deletion_log()

        # Sirve para deshacer la acción de eliminado. Se almacenan 3 array de eliminaciones por cada columna
        self.current_action = 0 

    def set_current_action(self,val):
        self.current_action += val
        if self.current_action < 0:
            self.current_action = 0 
        if self.current_action > 2:
            self.current_action = 2

    
        
    def create_selected_points(self):
        # Este diccionario almacena los puntos de cada selección. Después de cada selección se vacía usando el método reset_selected_points
        self.selected_points = {}
        for col in self.data.columns[1:]:
            self.selected_points[col] = []

    def reset_selected_points(self):
        for col in self.data.columns[1:]:
            self.selected_points[col] = []

    def create_deletion_log(self):
        # Este diccionario almacena los puntos de cada selección y registra las 3 últimas elminaciones de cada columna
        self.deletion_log = {}
        self.current_action = 0
        for col in self.data.columns[1:]:
            self.deletion_log[col] = {
                "idxs": [],
                0: [], # Accion 0
                1: [], # Accion 1
                2: [] # Accion 2   
            }
             
    # METODO PARA CONFIGURAR ESTILO DE LINEAS
    def __set_lines_config(self):
        self.line_style = '-'
        self.marker_style = 'o'
        self.line_colors = {}
           
    # METODO PARA CONFIGURAR ESTILO DEL AXEE
    def __set_ax_config(self):
        # Configurar el gráfico
        self.ax.set_xlabel('Fecha y Hora')
        self.ax.set_ylabel('Valores')
        self.ax.set_title('Gráfico interactivo - Selecciona columnas para mostrar')
        self.ax.grid(True,alpha=0.3)
        self.ax.set_xlim(self.tspan.min(), self.tspan.max())
            
        # Formatear el eje x para fechas
        if len(self.tspan) > 0:
            try:
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
                for label in self.ax.xaxis.get_majorticklabels():
                    label.set_rotation(0)
            except:
                pass

    # METODO PARA CREAR LA INTERFAZ
    def create_main_frame(self):
        # Configurar la ventana principal
        self.root.title("Revisor de eliminados")
        self.root.geometry("1200x800")

        # Crear el frame principal
        main_frame = ttk.Frame(self.root, padding="0")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # main_frame: 2 filas, 3 columnas
        # Filas 0 y 1: equitativas
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        # Columnas 0 y 1: 90%, columna 2: 10%
        main_frame.columnconfigure(0, weight=9)
        main_frame.columnconfigure(1, weight=9)
        main_frame.columnconfigure(2, weight=1)

        # Frame para el gráfico (ocupa filas 0,1 y columnas 0,1)
        graph_frame = ttk.Frame(main_frame)
        graph_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.create_plot(graph_frame)

        # Frame para checkboxes (fila 0, columna 2)
        checkbox_frame = ttk.Frame(main_frame)
        checkbox_frame.grid(row=0, column=2, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.create_checkboxes(checkbox_frame)

        # Frame para botones (fila 1, columna 2)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=2, sticky=(tk.N, tk.E, tk.S, tk.W))
        # Configurar para centrar vertical y horizontalmente
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=1)
        button_frame.rowconfigure(2, weight=1)
        button_frame.rowconfigure(3, weight=1)
        button_frame.columnconfigure(0, weight=1)

        # Botón para activar/desactivar selección de puntos
        self.selecting_points = False# Crear el selector de rectángulo
        self.select_button = ttk.Button(button_frame, text="Seleccionar puntos", command=self.toggle_selector)
        self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')         

        # Botón eliminar seleccionados
        self.delete_button = ttk.Button(button_frame, text="Eliminar seleccionados", command=self.__eliminate_selected)
        self.delete_button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.delete_button.state(["disabled"])

        # Botón deshacer ultima acción (solo borrar)
        self.undo_button = ttk.Button(button_frame, text="Deshacer acción", command=self.__undo)
        self.undo_button.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        self.undo_button.state(["disabled"])

        # Botón restaurar puntos seleccionados
        restore_button = ttk.Button(button_frame, text="Restaurar puntos seleccionados")
        restore_button.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

        # Botón para cambiar intervalo de tiempo
        self.estado_boton_cambiar_intervalo = StateTicksMes() # Estado inicial
        self.cambiar_intervalo_btn = ttk.Button(button_frame, text="Poner ticks cada semana", command=self.cambiar_intervalo_tiempo) # Estados-> Hay 3: Cada mes, cada semana, cada 24 horas
        self.cambiar_intervalo_btn.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        self.cambiar_intervalo_tiempo() # Inicializa el estado del botón (llamar al contexto)

    def update_undo_button(self):
        if self.current_action == 0:
            self.undo_button.state(["disabled"])
        else:
            self.undo_button.state(["!disabled"])

    def update_delete_button(self,is_selected):
        if not is_selected:
            self.delete_button.state(["disabled"])
        else:
            self.delete_button.state(["!disabled"])

    def create_plot(self, parent):
        """Crea el área del gráfico"""
        # Crear figura matplotlib usando Figure en lugar de plt.subplots()
        self.fig = Figure()  # figsize=(10, 6)
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('white')

        cols = self.data.columns[1:]
        
        self.__set_lines_config()

        for col in cols:
            y_data = self.data[col]
            if pd.api.types.is_numeric_dtype(y_data):  # Si es numérico entonces...
                line, = self.ax.plot(self.tspan, y_data, 
                            linewidth=2, markersize=4, 
                            label=f'{col}', marker=self.marker_style,
                            linestyle=self.line_style,visible=False)
                self.line_colors[col] = line.get_color()
         
        # Configurar el gráfico
        self.__set_ax_config()
            
        # Ajustar el diseño
        self.fig.tight_layout()
        
        # Crear canvas de tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

         # Agregar barra de herramientas para zoom/pan
        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def cambiar_intervalo_tiempo(self): # Contexto
        self.estado_boton_cambiar_intervalo.cambiar(self)
        self.canvas.draw()

    def create_checkboxes(self, parent):
        """Crea checkboxes para seleccionar columnas"""
        # Obtener nombres de columnas (excluyendo la primera que es fechas)
        column_names = self.data.columns[1:].tolist()
        
        # Frame para los checkboxes
        checkbox_container = ttk.Frame(parent)
        checkbox_container.grid(row=0, column=0, sticky=(tk.W, tk.E))
        checkbox_container.columnconfigure(0, weight=1)
        
        # Crear un canvas con scrollbar para los checkboxes
        canvas = tk.Canvas(checkbox_container)
        scrollbar = ttk.Scrollbar(checkbox_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Crear checkboxes
        self.column_vars = {}
        for i, col in enumerate(column_names):
            var = tk.BooleanVar(value=False)
            self.column_vars[col] = var
            checkbox = ttk.Checkbutton(scrollable_frame, text=col, variable=var, 
                                     command=lambda c=col: self.on_checkbox_change(c))
            checkbox.grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Configurar el grid para que se expanda
        parent.columnconfigure(0, weight=1)
    
    def on_checkbox_change(self, column):
        """Maneja los cambios en los checkboxes"""
        if self.column_vars[column].get():
            if column not in self.selected_columns:
                self.selected_columns.append(column)
        else:
            if column in self.selected_columns:
                self.selected_columns.remove(column)
        
        self.plot_selected_checkbox()
    
    def plot_selected_checkbox(self):
            """Grafica las columnas seleccionadas"""
            # Verificar que haya columnas seleccionadas
            for line in self.ax.get_lines():
                    line.set_visible(line.get_label() in self.selected_columns)

            # Actualizar el canvas
            self.canvas.draw()


    def toggle_selector(self):
        self.rectangle_selector = RectangleSelector(self.ax, self.onselect)
        self.selecting_points = not self.selecting_points
        if self.selecting_points:
            self.rectangle_selector.set_active(True)
            self.select_button.config(text="Detener selección")
        else:
            self.rectangle_selector.set_active(False)
            self.select_button.config(text="Seleccionar puntos")
            self.rectangle_selector.disconnect_events()

    def onselect(self,eclick, erelease):
        is_selected = False # Variable para saber si hay puntos seleccionados
        
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        for col in self.selected_columns:
            df_filtrado = self.data[(self.data[col] >= y1) & (self.data[col] <= y2) & (self.data[self.tspan_var_name] >= x1) & (self.data[self.tspan_var_name] <= x2)]
            idxs = df_filtrado.index
            if not df_filtrado.empty:
                for idx in idxs:
                    if idx in self.selected_points[col]:
                        self.selected_points[col].remove(idx)
                    else:
                        self.selected_points[col].append(idx)
                self.update_selected_in_plot(col)        

            if len(self.selected_points[col]) > 0:
                is_selected = True  

        self.update_delete_button(is_selected)


    def update_selected_in_plot(self,col):
        """Actualiza el gráfico mostrando los puntos seleccionados en cada columna"""
        # Si existe el scatter de esa columna, eliminarlo
        for artist in self.ax.collections:
            if artist.get_label() == f'selected_{col}':
                artist.remove()
                break

        # Filtrar el DataFrame por los índices seleccionados
        df_filtrado = self.data.loc[self.selected_points[col]]
        x = df_filtrado[self.tspan_var_name]
        y = df_filtrado[col]
        # Dibujar los puntos seleccionados
        self.ax.scatter(x, y, s=80, facecolors='none', edgecolors='red', linewidths=2, label=f'selected_{col}')
        self.canvas.draw()
    
    
    def __eliminate_selected(self):
        """Elimina los puntos seleccionados del DataFrame"""
        iseliminated = False
        for col in self.selected_points.keys():
            if self.selected_points[col]:
                self.data.loc[self.selected_points[col], col] = np.nan
                self.deletion_log[col]["idxs"].extend(self.selected_points[col])
                self.deletion_log[col][self.current_action] = self.selected_points[col].copy()
                iseliminated = True
        
        if iseliminated:
            self.reset_selected_points()
            self.set_current_action(1)
            self.update_undo_button()
            self.update_plot()
            self.update_delete_button(False) # Deshabilitar botón eliminar porque ya no hay puntos seleccionados

    def __undo(self):
        """Deshace la última acción de eliminación"""
        self.set_current_action(-1)

        for col in self.deletion_log.keys():
            if len(self.deletion_log[col][self.current_action]) > 0:
                idxs = self.deletion_log[col][self.current_action]
                print("ANTES")
                print(self.data.loc[idxs, col])
                self.data.loc[idxs, col] = self.data_backup.loc[idxs, col]

                print("DESPUES")
                print(self.data.loc[idxs, col])
        
        self.update_undo_button()
        self.update_plot()
        
        

    def update_plot(self):
        # Elimina las líneas
        for line in self.ax.get_lines():
            line.remove()

        # Elimina los puntos seleccionados (rojos)
        for artist in self.ax.collections:
            artist.remove()
        
        # Grafica de nuevo las líneas 
        for col in self.data.columns[1:]:
            y_data = self.data[col]
            if pd.api.types.is_numeric_dtype(y_data):  # Si es numérico entonces...
                self.ax.plot(self.tspan, y_data, 
                            linewidth=2, markersize=4, 
                            label=f'{col}', marker=self.marker_style,
                            linestyle=self.line_style, color= self.line_colors[col], visible=False)

        self.plot_selected_checkbox()
    
    # Configurar cierre de la aplicación
    def on_closing(self):
        self.root.destroy()


# Interfaz común de estados para el botón de cambiar intervalo de tiempo
class TickState: 
    def cambiar(self, contexto):
        raise NotImplementedError

# Estado 1: ticks cada mes
class StateTicksMes(TickState):
    def cambiar(self, contexto):
        contexto.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        contexto.cambiar_intervalo_btn.config(text="Poner ticks cada semana")
        contexto.estado_boton_cambiar_intervalo = StateTicksSemana()

# Estado 2: ticks cada semana
class StateTicksSemana(TickState):
    def cambiar(self, contexto):
        contexto.ax.xaxis.set_major_locator(mdates.HourLocator(interval=24*7))
        contexto.cambiar_intervalo_btn.config(text="Poner ticks cada 24 horas")
        contexto.estado_boton_cambiar_intervalo = StateTicksDia()


# Estado 3: ticks cada 24 horas
class StateTicksDia(TickState):
    def cambiar(self, contexto):
        contexto.ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
        contexto.cambiar_intervalo_btn.config(text="Poner ticks cada mes")
        contexto.estado_boton_cambiar_intervalo = StateTicksMes()