from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class LoginPage:

    def __init__(self, driver):
        self.driver = driver     
        # self.popup_button_classname = "css-47sehv"
        self.privacy_button_classname = "css-1hy2vtq"
        self.username_textbox_id = "bgcdw_login_form_username"
        self.password_textbox_id = "bgcdw_login_form_password"
        self.save_exit_form_id = "qc-cmp2-ui"
        self.save_exit_button_classname = "qc-cmp2-hide-desktop"
    
    def enter_data(self, username, password, APP):
        
        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, self.privacy_button_classname)))
        
        # self.driver.find_element_by_class_name(self.popup_button_classname).click()
        self.driver.find_element_by_class_name(self.privacy_button_classname).click()
        APP.progress_bar['value'] += APP.progress_count
        self.driver.find_element_by_id(self.username_textbox_id).clear()
        self.driver.find_element_by_id(self.username_textbox_id).send_keys(username)
        APP.progress_bar['value'] += APP.progress_count
        self.driver.find_element_by_id(self.password_textbox_id).clear()
        self.driver.find_element_by_id(self.password_textbox_id).send_keys(password)
        APP.progress_bar['value'] += APP.progress_count

    def save_exit_panel(self):
        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.ID, self.save_exit_form_id)))
        self.driver.find_element_by_class_name(self.save_exit_button_classname).click()
        # THIS IS NOT WORKING

    def click_login(self):
        self.driver.find_element_by_id(self.password_textbox_id).send_keys(Keys.ENTER)