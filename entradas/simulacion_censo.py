# TITULO: Sistema de Simulación Demográfica Masiva
# AUTOR: Ing. René Rosendo
# FECHA: 21 de Enero 2025
# TEMA: Algoritmos de Proyección Poblacional v2.0
# -----------------------------------------------------------------------------
# ESTE DOCUMENTO CONTIENE CÓDIGO FUENTE DE ALTA COMPLEJIDAD
# DESTINADO A PRUEBAS DE RENDERIZADO Y PAGINACIÓN AUTOMÁTICA.
# -----------------------------------------------------------------------------

import os
import sys
import time
import random
import math
import datetime
from collections import defaultdict, namedtuple

# =============================================================================
# CONFIGURACIÓN GLOBAL Y CONSTANTES DEL SISTEMA
# =============================================================================

# Definición de cohortes demográficos para el análisis
COHORTES = {
    'INFANCIA': (0, 12),
    'ADOLESCENCIA': (13, 17),
    'JUVENTUD': (18, 29),
    'ADULTEZ': (30, 59),
    'VEJEZ': (60, 120)
}

# Factores de corrección estadística por región
FACTORES_REGIONALES = {
    'NORTE': 1.05,
    'SUR': 0.98,
    'CENTRO': 1.12,
    'BAJIO': 1.03,
    'COSTA': 0.99
}

CONFIGURACION_SIMULACION = {
    "iteraciones": 100000,
    "semilla_random": 42,
    "verbose": True,
    "exportar_csv": False,
    "ruta_salida": "/mnt/data/resultados/proyecciones_2025.csv"
}

# =============================================================================
# CLASES PRINCIPALES
# =============================================================================

class Individuo:
    """
    Representa a un ciudadano único dentro de la simulación.
    Almacena atributos demográficos, socioeconómicos y de vivienda.
    """
    
    def __init__(self, id_unico, edad, genero, region):
        self.id = id_unico
        self.edad = edad
        self.genero = genero
        self.region = region
        self.ingreso_mensual = 0.0
        self.empleado = False
        self.nivel_educativo = "No especificado"
        
        # Inicialización compleja de atributos derivados
        self._calcular_cohorte()
        self._asignar_perfil_economico()

    def _calcular_cohorte(self):
        """Determina el grupo poblacional basado en la edad actual."""
        for nombre, (min_e, max_e) in COHORTES.items():
            if min_e <= self.edad <= max_e:
                self.cohorte = nombre
                return
        self.cohorte = "DESCONOCIDO"

    def _asignar_perfil_economico(self):
        """
        Simula el ingreso basado en la región y la edad usando una
        distribución normal ajustada por factores locales.
        """
        base = 5000
        if self.cohorte == 'ADULTEZ':
            base = 15000
        elif self.cohorte == 'VEJEZ':
            base = 8000
            
        factor = FACTORES_REGIONALES.get(self.region, 1.0)
        variacion = random.uniform(0.8, 1.2)
        
        self.ingreso_mensual = base * factor * variacion

    def __repr__(self):
        return f"<Individuo {self.id} | {self.edad} años | {self.region}>"


class CensoSimulador:
    """
    Controlador principal de la simulación estocástica.
    Administra la población, aplica políticas de crecimiento y genera reportes.
    """
    
    def __init__(self, total_poblacion):
        self.total_objetivo = total_poblacion
        self.poblacion_actual = []
        self.estadisticas = defaultdict(int)
        self.tiempo_inicio = None
        
        print(f"[INFO] Inicializando simulador para {total_poblacion} habitantes.")

    def generar_poblacion(self):
        """
        Crea instancias de Individuo hasta alcanzar el objetivo.
        Utiliza procesamiento por lotes para optimizar memoria.
        """
        self.tiempo_inicio = time.time()
        regiones = list(FACTORES_REGIONALES.keys())
        
        print("[PROCESO] Iniciando generación de datos sintéticos...")
        
        for i in range(self.total_objetivo):
            edad = int(random.gammavariate(2, 15))
            if edad > 100: edad = 100
            
            genero = random.choice(['M', 'F'])
            region = random.choice(regiones)
            
            nuevo_ciudadano = Individuo(i, edad, genero, region)
            self.poblacion_actual.append(nuevo_ciudadano)
            
            # Actualizar estadísticas en tiempo real
            self.estadisticas['total'] += 1
            self.estadisticas[region] += 1
            
            if i % 5000 == 0:
                sys.stdout.write(f"\rProgreso: {i}/{self.total_objetivo}")
                sys.stdout.flush()
                
        print("\n[OK] Generación completada.")

    def calcular_metricas_avanzadas(self):
        """
        Realiza cálculos agregados sobre la población generada.
        Simula una carga de trabajo pesada de CPU.
        """
        suma_ingresos = 0
        conteo_adultos = 0
        
        for p in self.poblacion_actual:
            suma_ingresos += p.ingreso_mensual
            if p.cohorte == 'ADULTEZ':
                conteo_adultos += 1
                
        promedio = suma_ingresos / len(self.poblacion_actual) if self.poblacion_actual else 0
        
        return {
            "ingreso_promedio": promedio,
            "tasa_adultez": conteo_adultos / len(self.poblacion_actual)
        }

    def exportar_informe(self):
        """
        Genera un volcado de datos (simulado) y un resumen ejecutivo.
        """
        metricas = self.calcular_metricas_avanzadas()
        tiempo_total = time.time() - self.tiempo_inicio
        
        reporte = f"""
        ========================================
        REPORTE FINAL DE SIMULACIÓN INEGI 2025
        ========================================
        Población Simulada: {self.total_objetivo}
        Tiempo de Ejecución: {tiempo_total:.4f} seg
        
        Métricas Económicas:
        - Ingreso Promedio Nac.: ${metricas['ingreso_promedio']:.2f}
        - Proporción Fuerza Laboral: {metricas['tasa_adultez']:.2%}
        
        Distribución Regional:
        {dict(self.estadisticas)}
        ========================================
        """
        return reporte

# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

def main():
    """
    Función main que orquesta la ejecución del script.
    """
    try:
        random.seed(CONFIGURACION_SIMULACION['semilla_random'])
        
        # Instanciar simulador con una población pequeña para demo
        # En producción usar 1,000,000+
        sim = CensoSimulador(total_poblacion=25000)
        
        sim.generar_poblacion()
        resultado = sim.exportar_informe()
        
        print(resultado)
        
        # Simulación de post-procesamiento
        print("[INFO] Comprimiendo resultados...")
        time.sleep(0.5)
        print("[INFO] Enviando a base de datos centralizada...")
        time.sleep(0.5)
        print("[EXIT] Proceso finalizado exitosamente (Código 0).")
        
    except KeyboardInterrupt:
        print("\n[ERR] Simulación abortada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERR] Error crítico en tiempo de ejecución: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
