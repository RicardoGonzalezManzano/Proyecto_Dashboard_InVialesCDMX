# Incidentes Viales CDMX 2022–2024 — Dashboard interactivo

Proyecto final de **Aplicaciones para Análisis de Datos**.  
Desarrollado por:

* Antonio Zavala Julio
* González Manzano Ricardo

Para este proyecto hicimos un análisis de **503,339 incidentes viales** registrados por el C5 de la Ciudad de México entre enero de 2022 y febrero de 2024. El proyecto trata tanto la parte descriptiva como predictiva: primero entiende qué pasó y, con ese conocimiento, predice qué tipo de accidente es más probable según la zona y la hora. Todo esto se explora en un dashboard interactivo hecho con Streamlit.

> \\\*\\\*Demo en vivo:\\\*\\\* \\\_pega aquí la URL de Streamlit Cloud cuando despliegues\\\_

\---

## Decisiones de diseño

Las ideas que guían el proyecto:

**El proyecto va de la parte descriptiva a la predictiva.**  
Cada variable del modelo (hora, alcaldía, mes, fin de semana) se eligió porque el análisis descriptivo demostró que la distribución de accidentes cambia con ella. El predictivo formaliza ese conocimiento.

**Tratamos 7 tipos de incidentes viales en lugar de 14.**  
El dataset trae 14 subtipos, pero 6 concentran el \~99 %. Los agrupamos en 6 principales + "Otros": gráficos legibles y un modelo más estable, sin perder señal. Esta agrupación es la base de conocimiento de la clase `TipoAccidente`, que comparten los archivos `descriptivo.py` y `predictivo.py`.

**El Dashboard debe ser interactivo.**  
Con el fin de hacer el despliegue de información más dinámico, el usuario elige alcaldía, mueve la hora y los gráficos responden. Así cualquiera formula sus propias preguntas.

\---

## Estructura del proyecto

```
Proyecto/
├── \\\_\\\_init\\\_\\\_.py       # Declara el proyecto como paquete Python (expone clases principales)
├── app.py            # Dashboard interactivo (Streamlit + Plotly) → streamlit run app.py
├── main.py           # Pipeline offline (genera CSV/Parquet y PNGs del reporte)
├── limpieza.py       # Fase 1 — limpieza + exporta viales\\\_limpio.csv y .parquet
├── modelos.py        # Fase 2 — clases POO (incluye TipoAccidente / CatalogoTipos)
├── descriptivo.py    # Fase 3 — exporta las 6 gráficas estáticas (PNG)
├── predictivo.py     # Fase 4 — PredictorTipoAccidente (Naive Bayes + baseline)
│
├── datos/
│   ├── diccionario-incidentes-viales-c5.xlsx  # Diccionario de datos del CSV original
│   ├── inViales\\\_2022\\\_2024.csv                 # CSV original (no se sube: \\\~128 MB)
│   ├── revision\\\_datos.ipynb                   # Notebook de exploración inicial del dataset
│   ├── viales\\\_limpio.csv                      # Limpio completo (no se sube)
│   └── viales\\\_limpio.parquet                  # Versión ligera (\\\~9 MB) que usa el dashboard
│
│
├── requirements.txt
└── .gitignore
```

\---

## Las clases (POO)

El diagrama completo está en [`docs/UML\\\_clases.pdf`](docs/UML_clases.pdf). Tres capas:

|Capa|Clases|Rol|
|-|-|-|
|**dominio**|`UbicacionGeografica`, `ReporteC4`, `Incidente`, `Colonia`, `Alcaldia`|Modelan un incidente y su agregación geográfica (Incidente **compone** ubicación + reporte; Colonia **agrega** incidentes; Alcaldía **agrega** colonias).|
|**conocimiento**|`TipoAccidente`, `CatalogoTipos`|La base de conocimiento: agrupan los 7 tipos y calculan sus distribuciones (por hora, por alcaldía, % graves).|
|**predictivo**|`AnalisisZona`, `PredictorTipoAccidente`|Operan sobre el conocimiento para predecir.|

`TipoAccidente` es el puente entre módulos: el descriptivo la usa para la gráfica de pastel y el predictivo usa su distribución horaria como evidencia.

\---

## Análisis descriptivo — 6 preguntas, 6 tipos de gráfico

|#|Pregunta|Gráfico|
|-|-|-|
|1|¿Qué tipos predominan en una alcaldía?|**Pastel**|
|2|¿Dónde se concentran según la hora?|**Mapa de calor** + slider|
|3|¿Cómo cambia el volumen durante el día?|**Líneas / área**|
|4|¿Qué alcaldías tienen más y cuáles más graves?|**Barras**|
|5|¿La atención se relaciona con volumen/gravedad?|**Dispersión**|
|6|¿Crece la demanda año con año?|**Columnas agrupadas**|

\---

## Análisis predictivo — tipo de accidente más probable

Eliges **alcaldía + hora** y el sistema estima la probabilidad de cada uno de los 7 tipos, con **dos enfoques que se comparan**:

* **Baseline** — frecuencias condicionadas `P(tipo | alcaldía, hora)` leídas directo de los datos (el conocimiento descriptivo "crudo").
* **Modelo** — `Naive Bayes` categórico: la versión suavizada y generalizadora de esas frecuencias. No se usa Random Forest; Naive Bayes es la contraparte probabilística directa de las frecuencias, más interpretable para este problema.

> \\\*\\\*Nota honesta (hallazgo del proyecto):\\\*\\\* como "Choque sin lesionados" es el \\\~46 % de todos los casos, el modelo casi siempre lo elige como el más probable (accuracy ≈ 0.46, F1-macro bajo por el fuerte desbalance de clases). El valor del predictor no está en el \\\*argmax\\\* sino en la \\\*\\\*distribución de probabilidades\\\*\\\*: muestra, por ejemplo, que en Cuauhtémoc a las 19 h la probabilidad de \\\*Atropellado\\\* sube a \\\~16 % frente al \\\~10 % global. Eso es exactamente el conocimiento descriptivo, ahora cuantificado.

\---

## Cómo correrlo

**Opción 1 — Demo en línea (sin instalación)**  
Accede directamente desde el navegador: *pega aquí la URL de Streamlit Cloud cuando despliegues*

**Opción 2 — Correrlo en local**

Requisito: Python 3.10+.

```bash
# 1. Entorno virtual
python -m venv venv
venv\\\\Scripts\\\\activate          # Windows
source venv/bin/activate       # Mac / Linux

# 2. Dependencias
pip install -r requirements.txt

# 3a. Abrir el tablero interactivo (necesita datos/viales\\\_limpio.parquet)
streamlit run app.py

# 3b. (Opcional) Regenerar datos y gráficas del reporte
python main.py                  # limpieza → descriptivo → predictivo
python main.py --paso limpieza  # genera viales\\\_limpio.csv y .parquet
```

> El dashboard solo necesita `datos/viales\\\_limpio.parquet` (incluido en el repo). El CSV completo y el pipeline `main.py` solo hacen falta si quieres regenerar todo desde el original.

\---

## Dataset

|Campo|Valor|
|-|-|
|Fuente|C5 CDMX — datos abiertos ([datos.cdmx.gob.mx](https://datos.cdmx.gob.mx))|
|Período|2022 – 2024|
|Registros (limpios)|503,339|
|Tipos de incidentes viales (agrupados)|7 (6 principales + "Otros")|

\---

## Dependencias

`streamlit` · `pandas` · `numpy` · `plotly` · `scikit-learn` · `pyarrow`  
(+ `matplotlib` para las gráficas estáticas). Ver `requirements.txt`.

