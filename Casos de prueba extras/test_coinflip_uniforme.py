import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
test_case2 = ET.SubElement(test_cases, "testcase", name="Verificar Frecuencia de Resultados (Distribución Uniforme)")

# Descripción del caso de prueba
summary = ET.SubElement(test_case2, "summary")
summary.text = "Verificar que la frecuencia de resultados (Cara y Sello) sea aproximadamente uniforme tras 10 lanzamientos."

# Precondiciones
preconditions = ET.SubElement(test_case2, "preconditions")
preconditions.text = "1. El navegador debe estar abierto.\n2. La página de lanzamiento de moneda debe estar cargada."

# Pasos del caso de prueba
steps = ET.SubElement(test_case2, "steps")

# Paso 1: Lanzar la moneda 100 veces
step1 = ET.SubElement(steps, "step")
ET.SubElement(step1, "step_number").text = "1"
ET.SubElement(step1, "actions").text = "Hacer clic en el botón 'Lanzar' 10 veces."
ET.SubElement(step1, "expectedresults").text = "La frecuencia de 'Cara' y 'Sello' debe ser aproximadamente igual (diferencia no mayor al 10%)."

# Crear el árbol XML para los resultados de las pruebas
results = ET.Element("results")

# Configuración del driver
driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/html/coinflip.html")

# Obtener la fecha y hora actual para el timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Variables para conteo
count_heads = 0
count_tails = 0
num_trials = 10

try:
    # Realizar 10 lanzamientos de moneda
    for _ in range(num_trials):
        # Hacer clic en el botón 'Lanzar'
        flip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Lanzar']"))
        )
        flip_button.click()

        # Esperar a que la animación de la moneda termine
        time.sleep(5)

        # Obtener el texto del resultado de la moneda
        coin_result_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "coinResult"))
        ).text

        # Extraer el resultado (Cara o Sello) del texto
        if "CARA" in coin_result_text:
            count_heads += 1
        elif "SELLO" in coin_result_text:
            count_tails += 1

    # Validar la distribución uniforme
    difference_percentage = abs(count_heads - count_tails) / num_trials * 100
    if difference_percentage <= 10:
        result = "p"
        comment = f"La distribución es uniforme: Cara={count_heads}, Sello={count_tails}."
    else:
        result = "f"
        comment = f"La distribución no es uniforme: Cara={count_heads}, Sello={count_tails}. Diferencia: {difference_percentage:.2f}%."

    # Crear el elemento XML para el resultado del caso de prueba
    testcase2_result = ET.SubElement(results, "testcase", external_id="CP-5")
    ET.SubElement(testcase2_result, "tester").text = "admin"
    ET.SubElement(testcase2_result, "timestamp").text = timestamp
    ET.SubElement(testcase2_result, "result").text = result
    ET.SubElement(testcase2_result, "notes").text = comment

    print(comment)
finally:
    driver.quit()

# Crear el archivo XML con los casos de prueba
tree_test_cases = ET.ElementTree(test_cases)
tree_test_cases.write("test_cases_coinflip_distribution.xml", encoding="UTF-8", xml_declaration=True)

# Crear el archivo XML con los resultados de las pruebas
tree_results = ET.ElementTree(results)
tree_results.write("test_results_coinflip_distribution.xml", encoding="UTF-8", xml_declaration=True)
