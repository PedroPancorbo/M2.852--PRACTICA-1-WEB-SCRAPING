# Extracción de ofertas de empleo 

## DOI

10.5281/zenodo.15157669

## Autores

- Pedro Jesús Pancorbo Rico  
- Pablo Rodríguez Moral  

---

## Archivos del repositorio

| Archivo                        | Descripción                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `jobs-scraping.py`            | Script principal para extraer, procesar y combinar datos de ofertas.        |
| `ofertas_empleo.csv`          | Archivo generado con los títulos de las ofertas.                            |
| `ofertas_globales.csv`        | Archivo generado con detalles adicionales de cada oferta.                   |
| `ofertas_completas.csv`       | Archivo final combinado con títulos y detalles.                             |
| `chromedriver.exe`            | Ejecutable del ChromeDriver necesario para Selenium en Windows.             |
| `LICENSE.chromedriver`        | Licencia de uso del ChromeDriver.                                           |
| `THIRD_PARTY_NOTICES.chromedriver` | Notas legales de terceros relacionadas con ChromeDriver.                |
| `requirements.txt`            | Lista de dependencias necesarias para ejecutar el script.                   |
| `README.md`                   | Este archivo, que describe el proyecto, uso y documentación relevante.      |

---

## Parámetros configurables en el script

Dentro del archivo `jobs-scraping.py`, puedes modificar los siguientes parámetros:

```python
output_titulos = "ofertas_empleo.csv"       # Archivo CSV para los títulos
output_datos = "ofertas_globales.csv"       # Archivo CSV para los detalles
output_final = "ofertas_completas.csv"      # Archivo combinado final

pagina_actual = 0                           # Página inicial (normalmente 0)
max_paginas = 200                           # Número de páginas a procesar

time.sleep(2)                               # Tiempo de espera entre interacciones

url_base = "https://empleate.gob.es/empleo/#/trabajo?search=*&pag="
