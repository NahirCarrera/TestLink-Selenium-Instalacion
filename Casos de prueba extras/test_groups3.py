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
    # **Caso 2: Número de participantes mayor al número de grupos**
    test_case2 = ET.SubElement(test_cases, "testcase", name="Número de participantes mayor al número de grupos")
    ET.SubElement(test_case2, "summary").text = "Verificar que los participantes se distribuyan equitativamente cuando el número de participantes es mayor al número de grupos."
    preconditions2 = ET.SubElement(test_case2, "preconditions")
    preconditions2.text = "1. El navegador debe estar abierto.\n2. La página de creación de grupos debe estar cargada."

    steps2 = ET.SubElement(test_case2, "steps")
    step2_1 = ET.SubElement(steps2, "step")
    ET.SubElement(step2_1, "step_number").text = "1"
    ET.SubElement(step2_1, "actions").text = "Ingresar 5 participantes y 2 grupos."
    ET.SubElement(step2_1, "expectedresults").text = "Los campos de texto aceptan los datos correctamente."

    step2_2 = ET.SubElement(steps2, "step")
    ET.SubElement(step2_2, "step_number").text = "2"
    ET.SubElement(step2_2, "actions").text = "Hacer clic en el botón 'Crear Grupos'."
    ET.SubElement(step2_2, "expectedresults").text = "Se generan 2 grupos con participantes distribuidos equitativamente."

    participants_textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "groupParticipants")))
    num_groups_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "numGroups")))

    participants_textarea.clear()
    participants_textarea.send_keys("Persona 1\nPersona 2\nPersona 3\nPersona 4\nPersona 5")
    num_groups_input.clear()
    num_groups_input.send_keys("2")

    create_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Crear Grupos']")))
    create_button.click()

    time.sleep(2)
    result_elements = driver.find_elements(By.XPATH, "//ul[@id='groupResults']/li")
    groups_text = [el.text.split(": ")[1].split(", ") for el in result_elements]

    total_participants = 5
    expected_group_count = 2
    min_participants_per_group = total_participants // expected_group_count
    max_participants_per_group = min_participants_per_group + 1

    valid_case2 = (
        len(result_elements) == expected_group_count and
        all(min_participants_per_group <= len(group) <= max_participants_per_group for group in groups_text)
    )

    if valid_case2:
        result = "p"
        comment = "Los participantes se distribuyeron correctamente entre los grupos."
    else:
        result = "f"
        comment = "Error: La distribución de los participantes entre los grupos no es correcta."

    testcase2_result = ET.SubElement(results, "testcase", external_id="CP-2")
    ET.SubElement(testcase2_result, "tester").text = "admin"
    ET.SubElement(testcase2_result, "timestamp").text = timestamp
    ET.SubElement(testcase2_result, "result").text = result
    ET.SubElement(testcase2_result, "notes").text = comment

    print(comment)

finally:
    driver.quit()

    # Guardar los resultados en XML
    tree_test_cases = ET.ElementTree(test_cases)
    tree_test_cases.write("test_case2_groups_3.xml", encoding="UTF-8", xml_declaration=True)

    tree_results = ET.ElementTree(results)
    tree_results.write("test_results_groups_3.xml", encoding="UTF-8", xml_declaration=True)
