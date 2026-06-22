# Incidentes Viales CDMX 2022-2024 - Dashboard interactivo

Proyecto final de Aplicaciones para Analisis de Datos.
Desarrollado por:

* Antonio Zavala Julio
* Gonzalez Manzano Ricardo

Para este proyecto hicimos un analisis de 503,339 incidentes viales registrados por el C5 de la Ciudad de Mexico entre enero de 2022 y febrero de 2024. El proyecto trata tanto la parte descriptiva como predictiva: primero entiende que paso y, con ese conocimiento, predice que tipo de accidente es mas probable segun la zona y la hora. Todo esto se explora en un dashboard interactivo hecho con Streamlit.

Demo en vivo: https://proyectodashboardinvialescdmx-kggtuejyu2h35zlzu4k3vk.streamlit.app/

\---

## Decisiones de diseno

Las ideas que guian el proyecto:

El proyecto va de la parte descriptiva a la predictiva.
Cada variable del modelo (hora, alcaldia, mes, fin de semana) se eligio porque el analisis descriptivo demostro que la distribucion de accidentes cambia con ella. El predictivo formaliza ese conocimiento.

Tratamos 7 tipos de incidentes viales en lugar de 14.
El dataset trae 14 subtipos, pero 6 concentran el 99%. Los agrupamos en 6 principales + "Otros": graficos legibles y un modelo mas estable, sin perder senal. Esta agrupacion es la base de conocimiento de la clase TipoAccidente, que comparten los archivos descriptivo.py y predictivo.py.

El Dashboard debe ser interactivo.
Con el fin de hacer el despliegue de informacion mas dinamico, el usuario elige alcaldia, mueve la hora y los graficos responden. Asi cualquiera formula sus propias preguntas.

\---

## Estructura del proyecto

Proyecto/
**init**.py         Declara el proyecto como paquete Python (expone clases principales)
app.py              Dashboard interactivo (Streamlit + Plotly) -> streamlit run app.py
main.py             Pipeline offline (genera CSV/Parquet)
limpieza.py         Fase 1 - limpieza + exporta viales\_limpio.csv y .parquet
modelos.py          Fase 2 - clases POO (incluye TipoAccidente / CatalogoTipos)
predictivo.py       Fase 3 - PredictorTipoAccidente (Naive Bayes + baseline)
requirements.txt
.gitignore

&#x20;   datos/
        diccionario-incidentes-viales-c5.xlsx   Diccionario de datos del CSV original
        inViales\_2022\_2024.csv                  CSV original (no se sube: \~128 MB)
        revision\_datos.ipynb                    Notebook de exploracion inicial del dataset
        viales\_limpio.csv                       Limpio completo (no se sube)
        viales\_limpio.parquet                   Version ligera (\~9 MB) que usa el dashboard


\---

## Las clases (POO)

|Capa|Clases|Rol|
|-|-|-|
|dominio|UbicacionGeografica, ReporteC4, Incidente, Colonia, Alcaldia|Modelan un incidente y su agregacion geografica|
|conocimiento|TipoAccidente, CatalogoTipos|Base de conocimiento: agrupan los 7 tipos y calculan distribuciones|
|predictivo|AnalisisZona, PredictorTipoAccidente|Operan sobre el conocimiento para predecir|

TipoAccidente es el puente entre modulos: el descriptivo la usa para la grafica de pastel y el predictivo usa su distribucion horaria como evidencia.

\---

## Analisis descriptivo - 6 preguntas, 6 tipos de grafico

# | Pregunta                                              | Grafico

\---|-------------------------------------------------------|--------
1  | Que tipos predominan en una alcaldia?                 | Pastel
2  | Donde se concentran segun la hora?                    | Mapa de calor + slider
3  | Como cambia el volumen durante el dia?                | Lineas / area
4  | Que alcaldias tienen mas y cuales mas graves?         | Barras
5  | La atencion se relaciona con volumen/gravedad?        | Dispersion
6  | Crece la demanda ano con ano?                         | Columnas agrupadas

\---

## Analisis predictivo - tipo de accidente mas probable

Eliges alcaldia + hora y el sistema estima la probabilidad de cada uno de los 7 tipos, con dos enfoques que se comparan:

Baseline: frecuencias condicionadas P(tipo | alcaldia, hora) leidas directo de los datos (el conocimiento descriptivo "crudo").

Modelo: Naive Bayes categorico, la version suavizada y generalizadora de esas frecuencias. No se usa Random Forest; Naive Bayes es la contraparte probabilistica directa de las frecuencias, mas interpretable para este problema.

Nota honesta: como "Choque sin lesionados" es el \~46% de todos los casos, el modelo casi siempre lo elige como el mas probable (accuracy 0.46, F1-macro bajo por el fuerte desbalance de clases). El valor del predictor no esta en el argmax sino en la distribucion de probabilidades: muestra, por ejemplo, que en Cuauhtemoc a las 19h la probabilidad de Atropellado sube a \~16% frente al \~10% global.

\---

## Como correrlo

Opcion 1 - Demo en linea (sin instalacion)
Accede directamente desde el navegador:
https://proyectodashboardinvialescdmx-kggtuejyu2h35zlzu4k3vk.streamlit.app/

Opcion 2 - Correrlo en local

Requisito: Python 3.10+

Paso 1 - Entorno virtual:
python -m venv venv
venv\\Scripts\\activate       (Windows)
source venv/bin/activate    (Mac / Linux)

Paso 2 - Instalar dependencias:
pip install -r requirements.txt

Paso 3 - Abrir el dashboard:
streamlit run app.py

El dashboard solo necesita datos/viales\_limpio.parquet (incluido en el repo).


\---

## Dataset

|Campo|Valor|
|-|-|
|Fuente|C5 CDMX - datos abiertos (datos.cdmx.gob.mx)|
|Periodo|2022 - 2024|
|Registros (limpios)|503,339|
|Tipos de incidentes viales|7 (6 principales + "Otros")|

\---

## Dependencias

streamlit, pandas, numpy, plotly, scikit-learn, pyarrow, matplotlib

Ver requirements.txt para versiones exactas.

