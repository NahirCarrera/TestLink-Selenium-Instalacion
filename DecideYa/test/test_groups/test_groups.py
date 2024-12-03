import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
# Caso de prueba: Verificar número de participantes menor al numero de grupos

# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
test_case1 = ET.SubElement(test_cases, "testcase", name="Verificar número de participantes menor al número de grupos")

# Descripción del caso de prueba
summary = ET.SubElement(test_case1, "summary")
summary.text = "Verificar que se muestra un mensaje de error al ingresar un número de participantes menor al número de grupos al crear los grupos."

# Precondiciones
preconditions = ET.SubElement(test_case1, "preconditions")
preconditions.text = "1. El navegador debe estar abierto.\n2. La página de creación de grupos debe estar cargada."

# Pasos del caso de prueba
steps = ET.SubElement(test_case1, "steps")

# Paso 1: Ingresar número de participantes menor que el número de grupos
step1 = ET.SubElement(steps, "step")
ET.SubElement(step1, "step_number").text = "1"
ET.SubElement(step1, "actions").text = "Ingresar menos participantes que el número de grupos (3 PARTICIPANTES, 7 GRUPOS)."
ET.SubElement(step1, "expectedresults").text = "Los campos de texto aceptan los datos correctamente."

# Paso 2: Hacer clic en el botón 'Crear Grupos'
step2 = ET.SubElement(steps, "step")
ET.SubElement(step2, "step_number").text = "2"
ET.SubElement(step2, "actions").text = "Hacer clic en el botón 'Crear Grupos'."
ET.SubElement(step2, "expectedresults").text = "Se muestra un mensaje de error."
# Crear el árbol XML para los resultados de las pruebas
results = ET.Element("results")

# Configuración del driver
driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/html/randomgroups.html") 

# Obtener la fecha y hora actual para el timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Ingresar menos participantes que el número de grupos
    participants_textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "groupParticipants"))
    )
    num_groups_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "numGroups"))
    )

    participants_textarea.send_keys("Persona 1\nPersona 2\nPersona 3")  # 3 participantes
    num_groups_input.send_keys("7")  # 7 grupos

    # Hacer clic en el botón 'Crear Grupos'
    create_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Crear Grupos']"))
    )
    create_button.click()

    # Esperar un momento para que el mensaje de error aparezca si existe
    time.sleep(2)
    

    # Capturar la pantalla y guardar la imagen como PNG
    driver.save_screenshot("test_groups_results.png")
    # Verificar si hay algún mensaje de error en el DOM (sin generar excepción si no lo encuentra)
    error_messages = driver.find_elements(By.XPATH, "//div[contains(text(),'No se puede crear los grupos')]")

    # Si el mensaje de error está presente
    if error_messages:
        result = "p"
        comment = "El sistema mostró el mensaje de error correctamente."
    else:
        result = "f"
        comment = "Error: No se mostró el mensaje de error."

    # Crear el elemento XML para el resultado del caso de prueba
    testcase1_result = ET.SubElement(results, "testcase", external_id="CP-5")
    ET.SubElement(testcase1_result, "tester").text = "admin"
    ET.SubElement(testcase1_result, "timestamp").text = timestamp
    ET.SubElement(testcase1_result, "result").text = result
    ET.SubElement(testcase1_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

# Crear el archivo XML con los casos de prueba
tree_test_cases = ET.ElementTree(test_cases)
tree_test_cases.write("test_cases_groups.xml", encoding="UTF-8", xml_declaration=True)

# Crear el archivo XML con los resultados de las pruebas
tree_results = ET.ElementTree(results)
tree_results.write("test_results_groups.xml", encoding="UTF-8", xml_declaration=True)
