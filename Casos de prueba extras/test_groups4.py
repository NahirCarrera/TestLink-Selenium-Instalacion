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
    # **Caso 3: Campos vacíos**
    test_case3 = ET.SubElement(test_cases, "testcase", name="Campos vacíos")
    ET.SubElement(test_case3, "summary").text = "Verificar que se muestre un mensaje de error al dejar los campos vacíos."
    preconditions3 = ET.SubElement(test_case3, "preconditions")
    preconditions3.text = "1. El navegador debe estar abierto.\n2. La página de creación de grupos debe estar cargada."

    steps3 = ET.SubElement(test_case3, "steps")
    step3_1 = ET.SubElement(steps3, "step")
    ET.SubElement(step3_1, "step_number").text = "1"
    ET.SubElement(step3_1, "actions").text = "Dejar los campos vacíos."
    ET.SubElement(step3_1, "expectedresults").text = "El sistema acepta los campos vacíos."

    step3_2 = ET.SubElement(steps3, "step")
    ET.SubElement(step3_2, "step_number").text = "2"
    ET.SubElement(step3_2, "actions").text = "Hacer clic en el botón 'Crear Grupos'."
    ET.SubElement(step3_2, "expectedresults").text = "Se muestra un mensaje de error indicando que se deben llenar los campos."

    participants_textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "groupParticipants")))
    num_groups_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "numGroups")))

    participants_textarea.clear()
    num_groups_input.clear()
    create_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Crear Grupos']")))
    create_button.click()

    time.sleep(2)
    alert = EC.alert_is_present()(driver)

    if alert and alert.text == "Debes ingresar al menos un participante y un número de grupos válido.":
        result = "p"
        comment = "El sistema mostró el mensaje de error correctamente."
        alert.accept()
    else:
        result = "f"
        comment = "Error: No se mostró el mensaje de error o el mensaje no es correcto."

    testcase3_result = ET.SubElement(results, "testcase", external_id="CP-3")
    ET.SubElement(testcase3_result, "tester").text = "admin"
    ET.SubElement(testcase3_result, "timestamp").text = timestamp
    ET.SubElement(testcase3_result, "result").text = result
    ET.SubElement(testcase3_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

    # Guardar los resultados en XML
    tree_test_cases = ET.ElementTree(test_cases)
    tree_test_cases.write("test_cases_groups_4.xml", encoding="UTF-8", xml_declaration=True)

    tree_results = ET.ElementTree(results)
    tree_results.write("test_results_groups_4.xml", encoding="UTF-8", xml_declaration=True)
