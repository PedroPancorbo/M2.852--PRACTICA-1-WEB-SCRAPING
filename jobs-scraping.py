from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# === Configuración global ===
output_titulos = "ofertas_empleo.csv"
output_datos = "ofertas_globales.csv"
output_final = "ofertas_completas.csv"

# URL base de la página (por ejemplo, la página 0)
url_base = "https://empleate.gob.es/empleo/#/trabajo?search=*&pag="

# === Función para extraer títulos de 200 páginas ===
def extraer_titulos():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        titulos = []
        pagina_actual = 0  # Inicia en la página 0
        max_paginas = 200  # Procesamos 200 páginas

        while pagina_actual < max_paginas:
            url = url_base + str(pagina_actual)
            driver.get(url)

            # Esperamos a que los títulos estén visibles
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.title-long-item.ng-binding'))
            )

            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Extraemos los títulos de la página actual
            elementos = driver.find_elements(By.CSS_SELECTOR, 'span.title-long-item.ng-binding')
            if not elementos:
                print(f"⚠️ No se encontraron títulos en la página {pagina_actual + 1}")
                break

            for e in elementos:
                texto = e.text.strip()
                if texto:
                    titulos.append(texto)

            print(f"✅ Página {pagina_actual + 1} procesada, {len(elementos)} títulos encontrados.")

            # Hacer clic en el botón "Siguiente" para ir a la siguiente página, si no es la última
            if pagina_actual < max_paginas - 1:
                siguiente_button = driver.find_element(By.CSS_SELECTOR, 'li.clickable a[title="Siguiente"]')
                siguiente_button.click()

                # Esperamos a que la página se cargue después de hacer clic en "Siguiente"
                time.sleep(5)

            pagina_actual += 1  # Incrementa la página para la siguiente iteración

        # Guardamos los títulos extraídos en un archivo CSV
        with open(output_titulos, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Título de la oferta"])
            for t in titulos:
                writer.writerow([t])

        print(f"✅ Títulos guardados en: {output_titulos}")
    finally:
        driver.quit()

# === Función para extraer propiedades de 200 páginas ===
def extraer_propiedades():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    resultados = []
    try:
        pagina_actual = 0
        max_paginas = 200  # Procesamos 200 páginas

        while pagina_actual < max_paginas:
            url = url_base + str(pagina_actual)
            driver.get(url)

            # Esperamos a que los títulos estén visibles
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.title-long-item.ng-binding'))
            )

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            tarjetas = driver.find_elements(By.CSS_SELECTOR, "div.row div.col-xs-12")

            for tarjeta in tarjetas:
                try:
                    span_title = tarjeta.find_element(By.CSS_SELECTOR, "span.title-long-item.ng-binding")
                    id_oferta = span_title.get_attribute("name").strip()

                    texto_completo = tarjeta.find_element(By.CSS_SELECTOR, "p.ng-binding").text.strip()
                    partes = texto_completo.split("\n")[0]
                    palabras = partes.split(" ")

                    fecha_idx = next(i for i, p in enumerate(palabras) if "/" in p)
                    fecha = palabras[fecha_idx]
                    localizacion = " ".join(palabras[:fecha_idx]).strip() or "Sin especificar"

                    resto = palabras[fecha_idx + 1:]
                    formaciones_inicio = [
                        "Otros", "Estudios", "Títulos", "Enseñanzas", "Sin", "Grados", "Nivel", "Doctorado"
                    ]

                    try:
                        form_idx = next(
                            i for i, word in enumerate(resto)
                            if word in formaciones_inicio
                        )
                        salario = " ".join(resto[:form_idx]).strip()
                        formacion = " ".join(resto[form_idx:]).strip()
                    except:
                        salario = " ".join(resto).strip()
                        formacion = ""

                    if not salario:
                        salario = "Sin especificar"

                    resultados.append([localizacion, fecha, salario, formacion, id_oferta])

                except:
                    continue

            print(f"✅ Página {pagina_actual + 1} procesada")

            # Hacer clic en el botón "Siguiente" para ir a la siguiente página, si no es la última
            if pagina_actual < max_paginas - 1:
                siguiente_button = driver.find_element(By.CSS_SELECTOR, 'li.clickable a[title="Siguiente"]')
                siguiente_button.click()

                # Esperamos a que la página se cargue después de hacer clic en "Siguiente"
                time.sleep(5)

            pagina_actual += 1  # Incrementa la página para la siguiente iteración

        with open(output_datos, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Localización", "Fecha", "Salario", "Formación", "ID"])
            writer.writerows(resultados)

        print(f"✅ Propiedades guardadas en: {output_datos}")
    finally:
        driver.quit()

# === Función para combinar títulos y propiedades ===
def combinar_titulos_y_datos():
    titulos = []
    datos = []

    with open(output_titulos, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                titulos.append(row[0].strip())

    with open(output_datos, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                datos.append(row)

    # Comprobamos que ambos tengan el mismo tamaño
    if len(titulos) != len(datos):
        print(f"❌ Advertencia: El número de títulos ({len(titulos)}) no coincide con el número de datos ({len(datos)})")

    # === Comprobaciones de integridad ===
    ids_vistas = set()
    for i in range(len(titulos)):
        # Comprobamos que no haya ID repetidas
        if datos[i][4] in ids_vistas:
            print(f"⚠️ Advertencia: ID repetida encontrada: {datos[i][4]} en el índice {i}")
        ids_vistas.add(datos[i][4])

        # Comprobamos que no haya campos vacíos
        if any(not campo for campo in [titulos[i], *datos[i]]):
            print(f"⚠️ Advertencia: Campo vacío encontrado en la fila {i + 1}")

    # === Comprobación de 10 resultados por página ===
    if len(titulos) != 2000:  # 10 resultados por página, 200 páginas
        print(f"⚠️ Advertencia: El número de resultados no es 2000. Se encontraron {len(titulos)} resultados.")

    # === Ajuste en la columna E ===
    for i in range(len(datos)):
        # Si la columna E (Formación) comienza con "Sin especificar", la ajustamos
        if datos[i][3].startswith("Sin especificar"):
            datos[i][3] = datos[i][3].replace("Sin especificar", "").strip()

    # Guardar el archivo final, incluso si hay advertencias
    with open(output_final, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Título", "Localización", "Fecha", "Salario", "Formación", "ID"])
        for i in range(len(titulos)):
            writer.writerow([titulos[i]] + datos[i])

    print(f"✅ Archivo final combinado guardado en: {output_final}")

# === MAIN ===
def main():
    print("▶️ Ejecutando extracción de títulos...") 
    extraer_titulos()

    print("▶️ Ejecutando extracción de propiedades...")
    extraer_propiedades()

    print("▶️ Combinando archivos...")
    combinar_titulos_y_datos()

    print("🎉 Proceso completo.")

if __name__ == "__main__":
    main()
