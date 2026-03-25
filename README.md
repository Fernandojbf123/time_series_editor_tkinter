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

### 2. Instalar UV (si aún no lo tienes)

UV es un manejador de paquetes Python ultra-rápido escrito en Rust. Si no lo tienes instalado:

#### En PowerShell:
```powershell
pip install uv
```

#### En Git Bash o Linux:
```bash
pip install uv
```

Después de instalar, cierra y vuelve a abrir tu terminal.

### 3. Crear el ambiente virtual e instalar dependencias

UV simplifica el proceso al crear el ambiente e instalar las dependencias en un solo paso:
En la carpeta del proyecto ejecuta el comando: 

#### En PowerShell o Git Bash:
```powershell
uv sync
```

Este comando:
- Lee las dependencias del archivo `pyproject.toml`
- Crea automáticamente el ambiente virtual en `.venv`
- Instala todas las librerías necesarias:
  - pandas (>=3.0.1)
  - numpy (>=2.4.3)
  - matplotlib (>=3.10.8)
  - netCDF4 (>=1.7.4)
  - scipy (>=1.17.1)
  - ipykernel (>=7.2.0)
  - tkinter (incluido con Python)

**Nota**: No necesitas activar manualmente el ambiente virtual. UV lo gestiona automáticamente.

### 4. Ejecutar el proyecto
Asegúrate de que el ambiente virtual está activo, se debería ver (time-series-editor-tkinter) en la terminal

Sino se ha activado ejecuta:
#### En PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

**Nota**: Si obtienes un error de permisos, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### En Git Bash o Linux:
```bash
source .venv/bin/activate
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
   
   Con pip:
   ```bash
   pip install pandas numpy matplotlib netcdf4 scipy ipykernel
   ```
   
   O con conda:
   ```bash
   conda install pandas numpy matplotlib netcdf4 scipy ipykernel
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

- Python 3.14.3
- Sistema operativo: Windows, macOS o Linux
- Git (para clonar el repositorio)

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de investigación.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request en GitHub y recuerda trabajar en una rama diferente a main.

## Contacto

Para preguntas o sugerencias, abre un issue en el repositorio de GitHub.
