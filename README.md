# Orquestador de Reportes Automatizados

**Versión:** 1.0.0  
**Stack:** Python 3, Pandoc, Docker/Podman, LaTeX, R

## 1. Descripción General

Este proyecto es una herramienta de **automatización documental** diseñada para convertir códigos fuente y documentos técnicos (`.py`, `.R`, `.ipynb`, `.tex`, `.md`) en reportes oficiales de Microsoft Word (`.docx`) altamente estilizados.

El sistema automatiza el flujo de trabajo de generación de documentación técnica, asegurando que el código, las ecuaciones y el análisis narrativo se presenten bajo una identidad visual institucional estricta.

### ¿Cómo funciona?
El orquestador utiliza un enfoque híbrido:
1.  **Pandoc + Lua Filters:** Convierte el contenido crudo y renderiza ecuaciones matemáticas.
2.  **Python-docx + XML Injection:** Post-procesa el archivo Word para inyectar imágenes de encabezado "Full Bleed" (borde a borde) y configura reglas de paginación avanzadas (alternancia de estilos par/impar).

---

## 2. Características Principales

*  **Procesamiento por Lotes (Batch):** Detecta y procesa automáticamente múltiples archivos de entrada simultáneamente.
*  **Soporte Multi-formato:**
    * **Python (.py) & R (.R):** Extrae metadatos y formatea el código con resaltado de sintaxis.
    * **Jupyter Notebooks (.ipynb):** Renderiza celdas de código y markdown.
    * **LaTeX (.tex):** Convierte ecuaciones complejas a formato nativo de Word.
    * **Markdown (.md):** Procesa texto enriquecido estándar.
---

## 3. Estructura del Proyecto

Para que el contenedor funcione correctamente, se debe respetar la siguiente estructura de directorios:

```text
/mi_proyecto
├── Containerfile          # Definición de la imagen del contenedor
├── orquestador.py         # Script principal 
├── entradas/              # [INPUT] Colocar aquí los archivos a procesar (.py, .tex, etc.)
├── archivos/              # [ASSETS] Recursos de configuración y diseño
│   ├── tpl_master.docx    # Plantilla base de Word (Estilos, Fuentes)
│   ├── section_break.lua  # Filtro Lua para gestión de secciones
│   ├── header_portada.png # Imagen: Portada (Hoja 1)
│   ├── header_tema.png    # Imagen: Título del Tema (Hoja 2)
│   ├── header_texto.png   # Imagen: Contenido Impares (Hoja 3, 5, 7...)
│   └── header_codigo.png  # Imagen: Contenido Pares (Hoja 4, 6, 8...)
└── tmp/                   # [TEMP] Carpeta de archivos intermedios (autogenerada)
```
---
## 4. Especificación de Metadatos (Encabezados)

El orquestador analiza las primeras 20 líneas de los archivos de código para extraer la información que llenará la Portada y la Hoja de Título.

Para que el sistema detecte los datos correctamente, debes usar el carácter de comentario correspondiente a cada lenguaje seguido de la palabra clave (ej. `TITULO:`, `AUTOR:`).

### Palabras Clave Aceptadas

- **TITULO:** Nombre principal del documento.  
- **AUTOR:** Nombre del responsable o Unidad Administrativa.  
- **FECHA:** Fecha de publicación o generación.  
- **TEMA:** Subtítulo o nombre específico del análisis (Hoja 2).  

### A. Para Python (.py) o R (.R)

```python
# TITULO: Análisis de Ingresos Trimestrales
# AUTOR: Dirección General de Estadísticas Económicas
# FECHA: 21 de Enero 2025
# TEMA: Comparativa Regional 2024-2025
# ---------------------------------------------------------
import pandas as pd
# ... el resto de tu código ...

### B. Para LaTeX (.tex)

```tex
% TITULO: Modelo de Simulación Demográfica
% AUTOR: Dr. René Rosendo
% FECHA: Enero 2025
% TEMA: Algoritmos Estocásticos Avanzados

\documentclass{article}
\begin{document}
% ... contenido ...

---

### C. Nota sobre Markdown (.md)

Si usas `.md` puro y quieres portada, debes incluir los estilos manualmente al inicio:

```markdown
::: {custom-style="TituloDocumento"}
Mi Título
:::

::: {custom-style="AutorUnidad"}
Dirección de Estadística
:::

::: {custom-style="FechaDocumento"}
Enero 2025
:::
---
## Estilos esperados en la plantilla Word ##

| Propósito            | Nombre del estilo   |
| -------------------- | ------------------- |
| Nombre del Documento | **TituloDocumento** |
| Autor y UA           | **AutorUnidad**     |
| Fecha                | **FechaDocumento**  |
| Título del Tema      | **TituloTema**      |
| Texto normal o Código| **TextoContenido**  |

---
## 5. Requisitos Previos
Docker o Podman instalado en el sistema host.

Las imágenes .png deben tener las dimensiones exactas del tamaño de hoja configurado en tpl_master.docx (ej. Carta o A4) para un ajuste perfecto.
---

## 6. Instalación y Construcción
### Usando Podman
podman build -t inegi-converter .

### Usando Docker
docker build -t inegi-converter .
---

## 7. Uso (Ejecución)
Para ejecutar el orquestador, monta el directorio actual al volumen /data del contenedor. Los reportes generados aparecerán en la raíz de la carpeta montada.
**En Linux / macOS:**
podman run --rm -v $(pwd):/data:Z inegi-converter

**En Windows (PowerShell):**
podman run --rm -v ${PWD}:/data:Z inegi-converter
---





