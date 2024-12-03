import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Crear el árbol XML para los casos de prueba
test_cases = ET.Element("testcases")
results = ET.Element("results")

driver = webdriver.Chrome()
driver.get("http://localhost/DecideYa/html/randomgroups.html")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # **Caso 1: Número de participantes igual al número de grupos**
    test_case1 = ET.SubElement(test_cases, "testcase", name="Número de participantes igual al número de grupos")
    ET.SubElement(test_case1, "summary").text = "Verificar que cada grupo tenga exactamente un participante cuando el número de participantes es igual al número de grupos."
    preconditions1 = ET.SubElement(test_case1, "preconditions")
    preconditions1.text = "1. El navegador debe estar abierto.\n2. La página de creación de grupos debe estar cargada."

    steps1 = ET.SubElement(test_case1, "steps")
    step1_1 = ET.SubElement(steps1, "step")
    ET.SubElement(step1_1, "step_number").text = "1"
    ET.SubElement(step1_1, "actions").text = "Ingresar 3 participantes y 3 grupos."
    ET.SubElement(step1_1, "expectedresults").text = "Los campos de texto aceptan los datos correctamente."

    step1_2 = ET.SubElement(steps1, "step")
    ET.SubElement(step1_2, "step_number").text = "2"
    ET.SubElement(step1_2, "actions").text = "Hacer clic en el botón 'Crear Grupos'."
    ET.SubElement(step1_2, "expectedresults").text = "Se generan 3 grupos, cada uno con un participante."

    participants_textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "groupParticipants")))
    num_groups_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "numGroups")))

    participants_textarea.clear()
    participants_textarea.send_keys("Persona 1\nPersona 2\nPersona 3")
    num_groups_input.clear()
    num_groups_input.send_keys("3")

    create_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Crear Grupos']")))
    create_button.click()

    time.sleep(2)
    result_elements = driver.find_elements(By.XPATH, "//ul[@id='groupResults']/li")

    valid_case1 = len(result_elements) == 3

    if valid_case1:
        result = "p"
        comment = "Los grupos se generaron correctamente con un participante por grupo."
    else:
        result = "f"
        comment = "Error: La distribución de los participantes en los grupos no es correcta."

    testcase1_result = ET.SubElement(results, "testcase", external_id="CP-1")
    ET.SubElement(testcase1_result, "tester").text = "admin"
    ET.SubElement(testcase1_result, "timestamp").text = timestamp
    ET.SubElement(testcase1_result, "result").text = result
    ET.SubElement(testcase1_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

    # Guardar los resultados en XML
    tree_test_cases = ET.ElementTree(test_cases)
    tree_test_cases.write("test_cases_groups_2.xml", encoding="UTF-8", xml_declaration=True)

    tree_results = ET.ElementTree(results)
    tree_results.write("test_results_groups_2.xml", encoding="UTF-8", xml_declaration=True)
