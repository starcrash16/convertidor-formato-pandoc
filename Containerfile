FROM debian:stable-slim

# Configuración de variables de entorno para evitar interacciones durante la instalación
# y definir la zona horaria correcta para los reportes.
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Mexico_City

# ----------------------------------------
# 1. Instalar dependencias del sistema
# ----------------------------------------
# Se actualizan los repositorios y se instalan herramientas esenciales:
# - python3/pip: Para ejecutar el orquestador.
# - pandoc: Núcleo de la conversión de formatos
# - texlive-*: Necesario para procesar archivos de entrada LaTeX (.tex).
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-docx \
        pandoc \
        tzdata \
        texlive \
        texlive-latex-extra \
        texlive-xetex \
        build-essential \
        python3-venv \
        python3-wheel && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ----------------------------------------
# 2. Instalar librerías Python externas
# ----------------------------------------
# docxcompose se utiliza para manipular documentos Word, pero no está en APT.
# Se utiliza el flag --break-system-packages porque las versiones recientes de Debian
# (Bookworm en adelante) implementan PEP 668 para proteger el entorno de Python del sistema.
RUN pip install --break-system-packages docxcompose

# ----------------------------------------
# 3. Configuración del entorno de trabajo
# ----------------------------------------
WORKDIR /usr/src/app

# Se copia el script local al contenedor.
# Nota: Aunque copiamos el archivo aquí, el CMD apunta a /data/orquestador.py,
# asumiendo que se montará un volumen en tiempo de ejecución.
COPY orquestador.py .

# ----------------------------------------
# 4. Comando de inicio
# ----------------------------------------
# Ejecuta el script principal desde el volumen montado en /data.
CMD ["python3", "/data/orquestador.py"]

