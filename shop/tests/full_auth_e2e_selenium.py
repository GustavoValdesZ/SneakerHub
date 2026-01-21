import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def human_delay(min_sec=0.5, max_sec=2.0):
    time.sleep(random.uniform(min_sec, max_sec))

def type_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def run_full_auth_test():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1200,1000")
    
    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # --- PHASE 1: REGISTRATION ---
        print("\n--- INICIANDO FASE 1: REGISTRO ---")
        driver.get("http://127.0.0.1:8000/register/")
        human_delay(1, 2)

        email_val = f"user.{random.randint(1000, 9999)}@test.com"
        password_val = "Password123!"

        print(f"Registrando usuario con email: {email_val}")
        
        type_human(driver.find_element(By.NAME, "first_name"), "Roberto")
        human_delay()
        type_human(driver.find_element(By.NAME, "last_name"), "Gomez")
        human_delay()
        type_human(driver.find_element(By.NAME, "email"), email_val)
        human_delay()
        type_human(driver.find_element(By.NAME, "password"), password_val)
        human_delay()
        type_human(driver.find_element(By.NAME, "confirm_password"), password_val)
        human_delay(1, 2)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        human_delay(2, 3)
        
        if "Hola, Roberto" in driver.page_source:
            print("Registro exitoso.")
        else:
            print("Error en el registro.")
            return

        # --- PHASE 2: LOGOUT ---
        print("\n--- INICIANDO FASE 2: CERRAR SESIÓN ---")
        human_delay(1, 2)
        logout_link = driver.find_element(By.LINK_TEXT, "Cerrar Sesión")
        logout_link.click()
        human_delay(2, 3)
        
        if "Iniciar Sesión" in driver.page_source:
            print("Sesión cerrada correctamente.")
        else:
            print("Error al cerrar sesión.")
            return

        # --- PHASE 3: LOGIN ---
        print("\n--- INICIANDO FASE 3: INICIAR SESIÓN ---")
        driver.get("http://127.0.0.1:8000/login/")
        human_delay(1, 2)

        print(f"Iniciando sesión con {email_val}...")
        type_human(driver.find_element(By.NAME, "email"), email_val)
        human_delay()
        type_human(driver.find_element(By.NAME, "password"), password_val)
        human_delay(1, 2)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        human_delay(2, 3)

        if "Hola, Roberto" in driver.page_source:
            print("¡Inicio de sesión exitoso! Flujo completo completado.")
        else:
            print("El inicio de sesión falló.")
            print(f"URL actual: {driver.current_url}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        human_delay(3, 5)
        driver.quit()

if __name__ == "__main__":
    run_full_auth_test()
