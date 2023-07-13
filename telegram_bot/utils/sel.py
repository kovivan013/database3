from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pydantic import BaseSettings

class Settings(BaseSettings):
    options = webdriver.ChromeOptions()

settings = Settings()

settings.options.add_argument("user-agent=fdghudf")

driver = webdriver.Chrome(options=settings.options)

try:
    # driver.get(url="https://www.roblox.com/login")
    # username_field = driver.find_element(By.ID, "login-username")
    # password_field = driver.find_element(By.ID, "login-password")
    # login_button = driver.find_element(By.CSS_SELECTOR, "button#login-button")
    # username: str = f"Kaktus345437"
    # password: str = "228Kaktus"
    # username_field.clear()
    # username_field.send_keys(username)
    # password_field.clear()
    # password_field.send_keys(password)
    # login_button.click()
    # time.sleep(5)
    driver.get(url="https://www.roblox.com/groups/4328109/Police-Roleplay-Community#!/about")
    time.sleep(4)


    roles_list = driver\
        .find_element(By.XPATH, "//group-members-list[@class=\"ng-scope ng-isolate-scope\"]")\
        .find_element(By.XPATH, ".//ul[@class=\"dropdown-menu\"]")\
        .find_elements(By.XPATH, ".//li")
    print([i.find_element(By.XPATH, ".//span[@class=\"text-overflow ng-binding\"]").get_attribute('textContent') for i in roles_list])


    # role_element = roles_ul_list.find_element(By.XPATH, ".//li[@id=\"role-42524605\"]").find_element(By.XPATH, ".//span[@class=\"role-member-count ng-binding ng-scope\"]")
    # print(role_element.get_attribute('textContent'))


    print("success")


    time.sleep(70000)
except Exception as err:
    print(err)
finally:
    driver.close()
    driver.quit()