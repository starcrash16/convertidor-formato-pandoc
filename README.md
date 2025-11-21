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

* 🚀 **Procesamiento por Lotes (Batch):** Detecta y procesa automáticamente múltiples archivos de entrada simultáneamente.
* 📄 **Soporte Multi-formato:**
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
├── orquestador.py         # Script principal (Lógica de negocio)
├── entradas/              # [INPUT] Colocar aquí los archivos a procesar (.py, .tex, etc.)
├── archivos/              # [ASSETS] Recursos de configuración y diseño
│   ├── tpl_master.docx    # Plantilla base de Word (Estilos, Fuentes)
│   ├── section_break.lua  # Filtro Lua para gestión de secciones
│   ├── header_portada.png # Imagen: Portada (Hoja 1)
│   ├── header_tema.png    # Imagen: Título del Tema (Hoja 2)
│   ├── header_texto.png   # Imagen: Contenido Impares (Hoja 3, 5, 7...)
│   └── header_codigo.png  # Imagen: Contenido Pares (Hoja 4, 6, 8...)
└── tmp/                   # [TEMP] Carpeta de archivos intermedios (autogenerada)
