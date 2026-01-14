# Time Series Plotter with Tkinter

Graficador interactivo de series de tiempo con interfaz gráfica en Tkinter y Matplotlib. Este proyecto permite visualizar, editar y corregir datos de series temporales de manera interactiva.

## Características

- 📊 **Visualización de múltiples series de tiempo**: Selecciona qué columnas graficar mediante checkboxes
- 🎯 **Selección de puntos**: Usa un selector rectangular para seleccionar puntos en el gráfico
- ❌ **Eliminación de valores**: Elimina puntos seleccionados de las series de tiempo
- ↩️ **Deshacer acciones**: Revierte las últimas 3 eliminaciones realizadas
- 🔄 **Restaurar puntos**: Compara series de datos corregidos vs datos sin corrección
- 📅 **Cambio de escala temporal**: Alterna entre ticks en el eje X por años, meses, semanas o días
- 💾 **Backup automático**: Mantiene una copia de seguridad de los datos originales

## Instalación

### 1. Descargar el proyecto desde GitHub

#### Opción A: Usando PowerShell

1. Abre PowerShell
2. Navega a la carpeta donde quieres descargar el proyecto:
   ```powershell
   cd C:\Users\TuUsuario\Documents
   ```
3. Clona el repositorio:
   ```powershell
   git clone https://github.com/Fernandojbf123/time_series_plotter_tkinter.git
   ```
4. Ingresa a la carpeta del proyecto:
   ```powershell
   cd time_series_plotter_tkinter
   ```

#### Opción B: Usando Git Bash

1. Abre Git Bash
2. Navega a la carpeta donde quieres descargar el proyecto:
   ```bash
   cd ~/Documents
   ```
3. Clona el repositorio:
   ```bash
   git clone https://github.com/Fernandojbf123/time_series_plotter_tkinter.git
   ```
4. Ingresa a la carpeta del proyecto:
   ```bash
   cd time_series_plotter_tkinter
   ```

### 2. Crear el ambiente virtual

#### En PowerShell:
```powershell
python -m venv .venv
```

#### En Git Bash o Linux:
```bash
python -m venv .venv
```

### 3. Activar el ambiente virtual

#### En PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

**Nota**: Si obtienes un error de permisos, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### En Git Bash o Linux:
```bash
source .venv/Scripts/activate
```

### 4. Instalar las dependencias

Con el ambiente virtual activado, ejecuta:

```powershell
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias:
- pandas
- numpy
- matplotlib
- tkinter (incluido con Python)

### 5. Ejecutar el proyecto

```powershell
python main.py
```

## Uso con Anaconda (ambiente base)

Si prefieres usar el ambiente base de Conda en lugar de crear un ambiente virtual:

1. **Abre Anaconda Prompt**

2. **Navega a la carpeta del proyecto**:
   ```bash
   cd C:\Users\TuUsuario\Documents\time_series_plotter_tkinter
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   
   O si prefieres usar conda:
   ```bash
   conda install pandas numpy matplotlib
   ```

4. **Ejecuta el proyecto**:
   ```bash
   python main.py
   ```

**Nota**: No es necesario crear ni activar ningún ambiente virtual si usas el ambiente base de Conda.

## Uso del Graficador

1. **Seleccionar columnas**: Marca los checkboxes de las series que deseas visualizar
2. **Seleccionar puntos**: Haz clic en "Seleccionar puntos" y dibuja un rectángulo sobre el área del gráfico
3. **Eliminar puntos**: Con puntos seleccionados (marcados en rojo), haz clic en "Eliminar seleccionados"
4. **Deshacer**: Haz clic en "Deshacer acción" para restaurar los últimos puntos eliminados (hasta 3 acciones)
5. **Cambiar escala temporal**: Usa el botón de intervalos de tiempo para alternar entre meses, semanas y días

## Estructura del Proyecto

```
time_series_plotter_tkinter/
│
├── main.py                 # Punto de entrada de la aplicación
├── prueba.py              # Clase principal del graficador interactivo
├── DataFrame_maker.py     # Funciones para crear y cargar DataFrames
├── Gra.py                 # Módulo de gráficos adicional
├── GraCorrector.py        # Módulo corrector de gráficos
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## Requisitos del Sistema

- Python 3.13.5
- Sistema operativo: Windows, macOS o Linux
- Git (para clonar el repositorio)

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de investigación.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request en GitHub.

## Contacto

Para preguntas o sugerencias, abre un issue en el repositorio de GitHub.
