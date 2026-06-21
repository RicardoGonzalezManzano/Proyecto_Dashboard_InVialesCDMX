"""
dashboard_incidentes
====================
Paquete de análisis y visualización de incidentes viales CDMX 2022-2024.

Módulos principales:
    modelos     — Clases POO y base de conocimiento
    limpieza    — Pipeline de limpieza del dataset original
    descriptivo — Análisis descriptivo y exportación de figuras
    predictivo  — Modelo predictivo (Naive Bayes + baseline)
    app         — Dashboard interactivo (Streamlit)
"""

from .modelos import CATEGORIAS_7, agregar_categoria
from .predictivo import PredictorTipoAccidente
