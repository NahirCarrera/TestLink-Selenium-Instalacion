import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Caso de prueba: Verificar Emparejamiento Participantes mayor a Premios
# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
test_case1 = ET.SubElement(test_cases, "testcase", name="Verificar Emparejamiento Participantes mayor a Premios")

# Descripción del caso de prueba
summary = ET.SubElement(test_case1, "summary")
summary.text = "Verificar que los premios se emparejen correctamente con los participantes y que no se incluyan participantes no ganadores en los resultados cuando la cantidad de participantes es mayor al número de premios."
# Precondiciones
preconditions = ET.SubElement(test_case1, "preconditions")
preconditions.text = "1. El navegador debe estar abierto.\n2. La página de emparejamiento debe estar cargada."

# Pasos del caso de prueba
steps = ET.SubElement(test_case1, "steps")

# Paso 1: Ingresar participantes y premios
step1 = ET.SubElement(steps, "step")
ET.SubElement(step1, "step_number").text = "1"
ET.SubElement(step1, "actions").text = "Ingresar una lista de participantes y premios en los campos correspondientes (4 PARTICIPANTES, 2 PREMIOS)."
ET.SubElement(step1, "expectedresults").text = "Los campos de texto aceptan los datos correctamente."

# Paso 2: Hacer clic en el botón 'Emparejar'
step2 = ET.SubElement(steps, "step")
ET.SubElement(step2, "step_number").text = "2"
ET.SubElement(step2, "actions").text = "Hacer clic en el botón 'Emparejar'."
ET.SubElement(step2, "expectedresults").text = "Se muestran los resultados con los premios emparejados con los participantes."

# Crear el árbol XML para los resultados de las pruebas
results = ET.Element("results")  # Esta línea se agregó para definir 'results'

# Configuración del driver
driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/html/pairing.html")  # Cambia por la ruta local de tu archivo pairing.html

# Obtener la fecha y hora actual para el timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Ingresar participantes
    participants = "Participante 1\nParticipante 2\nParticipante 3\nParticipante 4"
    prizes = "Premio 1\nPremio 2"
    
    participants_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "participants"))
    )
    participants_field.send_keys(participants)

    # Ingresar premios
    prizes_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "prizes"))
    )
    prizes_field.send_keys(prizes)

    # Hacer clic en el botón 'Emparejar'
    pair_button = driver.find_element(By.XPATH, "//button[normalize-space()='Emparejar']")
    pair_button.click()

    # Esperar 1 segundo para asegurarse de que los resultados se carguen
    time.sleep(1)

    # Capturar la pantalla y guardar la imagen como PNG
    driver.save_screenshot("pairing_results.png")

    # Verificar los resultados
    results_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#pairResults li"))
    )
    results_text = [result.text for result in results_list]
    
    # Validar que haya exactamente 3 resultados (igual al número de premios)
    expected_results = len(prizes.split("\n"))
    actual_results = len(results_text)

    result = "p" if actual_results == expected_results else "f"
    comment = (
        f"Resultados correctos: {results_text}" if result == "p"
        else f"Error: se esperaban {expected_results} emparejamientos, pero se encontraron {actual_results}."
    )

    # Crear el elemento XML para el resultado del caso de prueba
    testcase1_result = ET.SubElement(results, "testcase", external_id="CP-2")
    ET.SubElement(testcase1_result, "tester").text = "admin"
    ET.SubElement(testcase1_result, "timestamp").text = timestamp
    ET.SubElement(testcase1_result, "result").text = result
    ET.SubElement(testcase1_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

# Crear el árbol XML para los casos de prueba
tree_test_cases = ET.ElementTree(test_cases)
tree_test_cases.write("test_cases_pairing.xml", encoding="UTF-8", xml_declaration=True)

# Crear el archivo XML con los resultados de las pruebas
tree_results = ET.ElementTree(results)
tree_results.write("test_results_pairing.xml", encoding="UTF-8", xml_declaration=True)
