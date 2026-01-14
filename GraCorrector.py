import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mpl
from matplotlib.widgets import RectangleSelector, Button, CheckButtons
from matplotlib.dates import date2num, num2date

import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import messagebox


# %matplotlib qt


""" OBJETIVO 
CREAR UNA CLASE QUE RECIBA UN DATAFRAME


DEBE: 
    
    GRAFICAR CADA COLUMNA DEL DATAFRAME MEDIANTE CHECKBOX
    
    PERMITIR LA SELECCIÓN DE PUNTOS 
    RESALTAR LOS PUNTOS SELECCIONADOS CON UNA BOLITA ROJA

    
    BORRAR LOS PUNTOS DE LA COLUMNA SELECCIONADA
    
    NOTAS: SOLO SE PUEDEN BORRAR LOS PUNTOS DEL CHECKBOX ACTIVO
    
    DEBE TENER UN BOTON PARA GUARDAR EL DF CON LOS PUNTOS ELIMINADOS


    PENDIENTES: 
        CORREGIR EL ERROR AL COMPARAR FECHAS
        CREAR EL MÉTODO DEL CHECKBOX
        CREAR EL MÉTODO F1_KEY_DOWN (AYUDA)
        CREAR EL MÉTODO F5_KEY_DOWN (GUARDAR, historial de eliminacion y df en pkl o en csv)
        CREAR EL MÉTODO __GUARDAR_HISTORIAL Y LLAMARLO EVENTO KEY_DOWN
"""


class GraCorrector():
    def __init__(self,df):
        self.df = df
        self.df_original = self.df.copy() # respaldo del df original
        
        # Nombres de las columnas (lista de str)
        self.tspan_var_name = "tspan"
        self.cols = [col for col in df.columns if col != self.tspan_var_name] # todas las columnas que no sean X 

        # Variable X (recibo datetime y cambio a datenum: días desde el 1 de enero de 0001)
        self.x = date2num(df[self.tspan_var_name])
        self.df[self.tspan_var_name]= self.x
        
        self.active_labels = set()
        
        # diccionario con los puntos (tspan,val) seleecionados por cada columna, que se remarcan en rojo en el gráfico
        self.__create_dict_selected_points()
        
        
        
        
        
        
        
        # # Crear el historial de datos eliminados
        # self.__create_del_record()
    
        # #Crear el grafico
        # self.__create_figure()
        # self.__create_checkbox()

        # # Crear eventos 
        # self.rectangle_selector = None #Selector de rectángulo
        # self.__create_rectangle_selector() # selector de rectángulo
        # self.fig.canvas.mpl_connect("key_press_event",self.__on_key) #borrar puntos
        
        # Graficar        
        # self.__draw_figure()


    ########## MAKERs ##########   
    # C.1. Crear diccionario de datos seleccionados
    def __create_dict_selected_points(self):
        self.selected = {}
        for col in self.cols:
            self.selected[col] = {}
            self.selected[col]["points"] = np.empty((0, 2),dtype=float) 
            
    def __create_figure(self):
        self.fig, self.ax = plt.subplots(figsize=(10,6))
        self.xmin = self.x.min() - .1 # - .1 por el formato de date2num
        self.xmax = self.x.max() + .1

    # # C.2. Crear historia de eliminacion
    # def __create_del_record(self):
    #     self.del_record = pd.DataFrame({
    #         "Fecha_de_eliminacion": pd.Series([], dtype = "datetime64[ns]"),
    #         "variable":pd.Series([], dtype = "str"),
    #         "tspan":pd.Series([], dtype = "datetime64[ns]"),
    #         "valor":pd.Series([], dtype= "float"),
    #         })
    
    
    # ########## UPDATERs / SETTERs ##########  
    # # U.1. Update cols        
    # def __set_col_visible(self,col):
    #     # logica de presionar el checkbox: Siempre que se presione el checkbox se actualiza el df cropped
    #     self.lines[col].set_visible(not self.lines[col].get_visible())
        
    #     # self.fig.canvas.draw_idle() 
        
    # # U.2. Update historial
    # def __set_del_record(self,col,selected_x,selected_y):
    #     current_date = datetime.datetime.now()
    #     current_date = current_date.replace(second=0, microsecond=0)
        
    #     n_datos = selected_x.size
    #     new_del_record = pd.DataFrame({
    #         "Fecha_de_eliminacion": np.repeat(current_date,n_datos),
    #         "variable": np.repeat(col,n_datos),
    #         "tspan": selected_x,
    #         "valor": selected_y,
    #         })
        
    #     self.del_record = pd.concat([self.del_record, new_del_record], ignore_index=True)
        
    # def __update_checkboxes(self):
    #     if not hasattr(self, "checkbox"):
    #         self.__create_checkbox()
    #         return
    
    #     for i, col in enumerate(self.cols):
    #         line_visible = self.lines[col].get_visible()
    #         check_status = self.checkbox.get_status()[i]
    #     if line_visible != check_status:
    #         self.check.set_active(i)

    # ########## SOPORTE ##########  
    # #verificar si el punto ya fue seleccionado
    # def __is_in_selected(self,col,new_point):
    #     # col = nombre de la columna
    #     # new_point = (tspan[i], y[i])
    #     return new_point in self.selected[col]["points"]

    
    # ########## GRAFICO  ########## 
    
    # #D.1.
    # def __create_figure(self):
    #     self.fig, self.ax = plt.subplots(figsize=(10,6))
    #     self.xmin = self.x.min() - .1 # - .1 por el formato de date2num
    #     self.xmax = self.x.max() + .1
        
        
    # # D.2. CREAR GRAFICO
    # def __draw_figure(self):
        
    #     # Guardar visibilidad actual (si existía)
    #     visibilities = {col: self.lines[col].get_visible() for col in self.cols} if hasattr(self, "lines") else {}
   
    #     self.ax.clear() # borro el axe
        
    #     # Pasos:
    #     # 1. graficar los puntos de la columna que fueron seleccionados
    #     for col in self.cols:
    #         points = self.selected[col]["points"]
    #         if points.shape[0] > 0:
    #             selected_x = points[:,0]
    #             selected_y = points[:,1]
    #             self.ax.scatter(selected_x, selected_y, c='red', marker='o')
        
    #     # 2. graficar los puntos del df
    #     self.lines = {}
    #     for col in self.cols:
    #         p = self.ax.plot(self.x, self.df[col], marker='+', label=col, visible=False)
    #         self.lines[col] = p[0]
    #         if col in visibilities:
    #            self.lines[col].set_visible(visibilities[col])
        
    #     # 3. actualizar el checkbox
    #     # self.__update_checkboxes()
        
        
    #     # 4. Dar formato al grafico
    #     self.ax.set_xlim(self.xmin, self.xmax)
    #     self.ax.xaxis.set_major_formatter(mpl.DateFormatter('%Y-%m-%d'))
    #     self.ax.xaxis.set_major_locator(mpl.AutoDateLocator())
    #     # self.fig.autofmt_xdate()
        
    #     # 5. Reiniciar el selector de área. 
    #     # Nota: La figura y el selector persisten aunque se borre el ax.
    #     # Por eso se debe reiniciar el selector.
    #     self.__rectangle_destroy()
    #     self.__create_rectangle_selector()
        
    #     # 6. Dibujar
    #     self.fig.canvas.draw_idle()  


    # #D.3. CREAR SELECTOR
    # def __create_rectangle_selector(self):
    #     self.rectangle_selector = RectangleSelector(self.ax, self.__on_select)
    
    # #D.4. DESTRUIR SELECTOR
    # def __rectangle_destroy(self):
    #     #Destruir el evento y borrar el axe
    #     self.rectangle_selector.set_active(False)
    #     self.rectangle_selector.disconnect_events()
      
    # #D.5. Crear checkboxes
    # def __create_checkbox(self):
    #     # ax = self.ax
    #     cols = self.cols
    #     rax = self.ax.inset_axes([0.0, 0.0, 0.12, 0.2])
    #     checkbox = CheckButtons(
    #         ax = rax,
    #         labels = cols,
    #         )
    #     self.checkbox = checkbox
        
    #     #Creo el evento de escuchar el click en el checkbox
    #     self.checkbox.on_clicked(self.__set_col_visible)

    
    # ########## EVENTOS ##########
    # #E.1.  SELECCIONAR PUNTOS EN EL GRAFICO
    # def __on_select(self,eclick,erelease): 
    #     """
    #     Las propiedades eclick y erelease tienen datos (x,y) de donde se hace click y donde se suelta.
    #     Esto crea las coordenadas del rectángulo
    #     """
    #     xi = eclick.xdata # coord x del click
    #     yi = eclick.ydata # coord y del click
    #     xe = erelease.xdata # coord x al soltar click
    #     ye = erelease.ydata # coord y al soltar click
        
    #     #Crear un diccionario con los valores de tspan y de la columna seleccionados                             
    #     for col in self.cols:
    #         df_cropped = self.df[["tspan",col]]
    #         cond = (df_cropped["tspan"] >= xi ) & (df_cropped["tspan"] <= xe) & (df_cropped[col] >= yi) & (df_cropped[col] <= ye)
    #         df_cropped = df_cropped[cond]
            
    #         # recupero puntos guardados para la columna
    #         points = self.selected[col]["points"]
            
    #         if not (df_cropped.empty): # si tiene datos
    #             new_tspan = list(df_cropped.iloc[:,0])
    #             new_y = list(df_cropped.iloc[:,1])
                
    #             for idx in range(0,len(new_y)):
    #                 new_point = (new_tspan[idx], new_y[idx])
                    
    #                 if self.__is_in_selected(col, new_point): # si el punto existe en selected removerlo
    #                     points = points[~np.all(points == new_point, axis=1)]
    #                 else: # si el punto no existe se agrega
    #                     points = np.vstack([points,new_point])
            
    #         self.selected[col]["points"] = points

    #     # self.__draw_figure()
        
    # # E.2. HACER CLICK EN UN CHECKBOX
    # def __on_checkbox_click(self,col):
        
    #     self.p

    # # E.3. KEY PRESS: hasta ahora son: "delete" para borrar, "f1" para ayuyda
    # # "u" para deshacer el borrado de un punto
    # def __on_key(self,event):
    #     # BORRAR PTS AL PRESIONAR delete / suprimir
    #     self.__delete_key_down(event)
        
    #     # DESHACER PUNTOS BORRADOS
    
    
    # # E.3.1.
    # def __delete_key_down(self,e):
    #     if e.key == "delete": 
    #         col_has_points = []
    #         col_points_count_to_delete = []
    #         lineas = ["Columna -- Cantidad de datos"]
    #         for col in self.cols: 
    #             points = self.selected[col]["points"]
    #             col_has_points.append(points.shape[0] > 0)
    #             col_points_count_to_delete = points.shape[0]
    #             lineas.append(f"{col} -- {col_points_count_to_delete}")
                
    #         texto_de_pregunta = "\n".join(lineas)
            
    #         # Confirmación de borrado de datos
    #         root = tk.Tk()
    #         root.withdraw()  # Oculta la ventana principal
    #         respuesta = messagebox.askquestion("Confirmar acción", f"¿Se borraran las siguientes cantidades de datos? \n {texto_de_pregunta}")
                
    #         if respuesta == "yes":
    #             for col in self.cols:  
    #                 points = self.selected[col]["points"]
                    
    #                 self.selected[col]["points"] = np.empty((0, 2),dtype=float) # borrar los puntos guardados
                    
    #                 if points.shape[0] > 0:
    #                     selected_x = points[:,0]
    #                     selected_y = points[:,1]
    #                     self.__set_del_record(col, selected_x, selected_y) #guardar ptos en el historial
    #                     for idx in range(0,len(selected_x)):
    #                         cond = (self.df["tspan"] == selected_x[idx]) & (self.df[col] == selected_y[idx])
    #                         self.df.loc[cond,col] = np.nan
                            
                        
    #             self.__draw_figure()

    
    #    # ########## GUARDADO EN HD ##########             
    #    # def __f5_key_down(self):

        