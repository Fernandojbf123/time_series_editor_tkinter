# Resumen del Proyecto - Time Series Plotter

## Descripción General
Aplicación de escritorio para visualizar y editar series de tiempo de manera interactiva usando Python, Tkinter y Matplotlib.

## Funcionalidades Principales

### Visualización
- Gráfico interactivo con múltiples series de tiempo
- Selección de columnas mediante checkboxes
- Zoom y navegación con herramientas de Matplotlib
- Cambio dinámico de escala temporal (años, meses, semanas, días)

### Edición de Datos
- **Selección rectangular de puntos**: Permite seleccionar regiones en el gráfico
- **Eliminación de valores**: Marca puntos seleccionados como NaN
- **Deshacer**: Hasta 3 acciones de eliminación
- **Backup automático**: Guarda copia de datos originales
- **Restaurar puntos**: Comparar datos corregidos vs originales

### Gestión de Datos
- Carga de datos desde archivos pickle
- Soporte para DataFrames de pandas
- Manejo de fechas con matplotlib.dates
- Combinación de múltiples series temporales

## Tecnologías Utilizadas
- **Python 3.8+**
- **Tkinter**: Interfaz gráfica
- **Matplotlib**: Visualización de gráficos
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas

## Arquitectura

### Módulos Principales
- `prueba.py`: Clase InteractivePlotterTk (graficador principal)
- `DataFrame_maker.py`: Funciones de creación y carga de datos
- `Gra.py`: Módulo de gráficos auxiliar
- `GraCorrector.py`: Corrector de gráficos
- `main.py`: Punto de entrada (no rastreado en Git)

### Patrón de Diseño
- **State Pattern**: Para manejo de intervalos de tiempo (StateTicksMes, StateTicksSemana, StateTicksDia)
- **Event-driven**: Callbacks de Tkinter para interactividad
- **MVC**: Separación entre datos (DataFrame), vista (Tkinter/Matplotlib) y control (InteractivePlotterTk)

## Flujo de Trabajo

1. **Carga de datos**: Desde pickle o creación de muestra
2. **Conversión temporal**: Fechas a números con mdates.date2num
3. **Renderizado**: Gráfico embebido en ventana Tkinter
4. **Interacción**: Selección, eliminación, deshacer
5. **Persistencia**: Backup automático para restauración

## Casos de Uso

### Corrección de Series Temporales
- Identificar y eliminar outliers
- Limpiar datos de sensores defectuosos
- Comparar datos antes/después de corrección

### Análisis de Datos Oceanográficos
- Temperatura, salinidad, corrientes marinas
- Múltiples profundidades
- Validación de datos de boyas

## Estado Actual

### Completado ✅
- Visualización interactiva
- Selección y eliminación de puntos
- Sistema de deshacer (3 niveles)
- Cambio de escala temporal
- Interfaz con checkboxes

### Pendiente 📋
- Historial de deshacer ilimitado
- Guardar DataFrame corregido (CSV, Excel, pickle)
- Restaurar puntos específicos (no solo deshacer)
- Graficado de variables vectoriales (Rap, Dir)
- Manejo especial para eliminación de U y V

## Instalación Rápida

```bash
git clone https://github.com/Fernandojbf123/time_series_plotter_tkinter.git
cd time_series_plotter_tkinter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Notas Técnicas

- Backend matplotlib: `Agg` (no interactivo) para evitar ventanas duplicadas
- Uso de `Figure()` en lugar de `plt.subplots()` para integración con Tkinter
- `FigureCanvasTkAgg` para embedding del gráfico
- `RectangleSelector` para selección de regiones
- Formato de fechas: `mdates.DateFormatter` y locators

## Autor
Fernando

## Repositorio
https://github.com/Fernandojbf123/time_series_plotter_tkinter
