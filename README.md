# Sistema de Análisis de Gastos

Sistema completo de gestión y análisis de gastos personales desarrollado en Python. Permite registrar, visualizar y analizar gastos mediante gráficos interactivos y cálculos estadísticos.

**Autor:** Gaspar Ramiro Sebastian  
**Universidad Católica de Salta** - Programación 2
**Examen Final**

---

## Descripción

Este programa permite administrar gastos personales de forma completa, ofreciendo:

- **Visualización gráfica** de gastos (líneas y barras)
- **Análisis estadístico** (totales, promedios, máximos, mínimos)
- **Gestión completa** (agregar, modificar, eliminar, visualizar)
- **Sistema de backups** automáticos
- **Validación de datos** robusta

---

## Requisitos

```bash
pip install numpy matplotlib
```

---

## Uso

```bash
python Examen_Final.py
```

El programa presenta un menú interactivo con las siguientes opciones:

### Gráficos
1. Gráfico de gastos por tiempo (plot)
2. Gráfico de gastos por tiempo (barras)
3. Gráfico de gastos por categoría

### Cálculos
4. Cálculos generales
5. Cálculos por categoría

### Gestión de Datos
6. Ver todos los gastos
7. Agregar nuevo/s gastos
8. Modificar un gasto
9. Eliminar un gasto

---

## Formato del archivo CSV

El programa lee y escribe datos en `GastosMensuales.csv` con la siguiente estructura:

```csv
año,mes,dia,categoria,precio,descripcion
2025,05,27,alimentación,150.75,bla
2025,06,23,transporte,50.0,bla
2025,07,11,entretenimiento,75.5,ejemplo
```

**Columnas:**
- `año`: Año del gasto (ej: 2025)
- `mes`: Mes del gasto (formato: 05, 12)
- `dia`: Día del gasto (formato: 07, 23)
- `categoria`: Categoría del gasto (alimentación, transporte, etc.)
- `precio`: Monto del gasto
- `descripcion`: Descripción opcional del gasto

---

## Características Principales

### Visualización
- Gráficos de línea para ver evolución temporal
- Gráficos de barras para comparaciones
- Análisis por día, mes, año o múltiples años
- Gráficos por categoría

### Análisis
- Cálculos con NumPy (suma, promedio, máximo, mínimo)
- Análisis general o por categoría específica
- Filtros por periodo (mensual/anual)

### Gestión
- **Agregar gastos** con validación completa de fechas
- **Modificar gastos** existentes manteniendo valores actuales
- **Eliminar gastos** con confirmación de seguridad
- **Ver todos** los gastos registrados
- **Backups automáticos** con timestamp antes de guardar cambios

### Validaciones
- Años entre 2000 y año actual
- Meses entre 1-12
- Días válidos según mes y año (incluye años bisiestos)
- Precios mayores a 0
- Confirmaciones antes de operaciones críticas

---

## Estructura del Proyecto

```
├── Examen_Final.py          # Programa principal
├── GastosMensuales.csv      # Base de datos
└── *.backup_*               # Backups automáticos
```

---

## Funciones Principales

### Visualización
- `grafico_gastos_generales_plot()` - Gráfico de líneas
- `grafico_gastos_generales_barra()` - Gráfico de barras  
- `grafico_gastos_por_categoria()` - Gráfico por categorías

### Análisis
- `calculos_generales()` - Estadísticas generales
- `calculos_especificos()` - Estadísticas por categoría

### CRUD
- `agregar_gasto()` - Añadir nuevo gasto
- `modificar_gasto()` - Editar gasto existente
- `eliminar_gasto()` - Borrar gasto
- `ver_gastos()` - Listar todos los gastos
- `guardar_csv()` - Guardar cambios con backup

### Auxiliares
- `analisis_csv()` - Leer datos del CSV
- `pedir_año_para_grafico()` - Validar entrada de año
- `pedir_mes_para_grafico()` - Validar entrada de mes

---

## Tecnologías Utilizadas

- **Python 3.7+**
- **NumPy** - Cálculos numéricos
- **Matplotlib** - Visualización de datos
- **CSV** - Lectura/escritura de datos
- **Calendar** - Validación de fechas
- **Datetime** - Timestamps y fechas
- **OS/Shutil** - Gestión de archivos y backups
