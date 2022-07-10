from selenium.common.exceptions import NoSuchElementException

class HomePage:

    def __init__(self, driver):
        self.driver = driver

        self.user_credit_id = "header_credits"
        self.user_uri_id = "header_uri"
        self.username_xpath = '//*[@id="userInfoSheet"]/div[1]'
        self.auction_id     = "trade_btn"

        # Expected Advertisements' xpath
        self.ads1 = '//*[@id="helix_lf4_close"]'
        self.ads2 = '//*[@id="bonus_sale_close"]'
        self.ads3 = '//*[@id="button_main"]'

    def close_ads(self, APP):
        
        try:
            self.driver.find_element_by_xpath(self.ads1).click()
            APP.print_log("Helix Lf4 adv is closed.")
        except Exception:
            APP.print_log("Helix Lf4 adv not found!.")
        APP.progress_bar['value'] += APP.progress_count
        try:
            APP.print_log("Bonus sale adv is closed.")
            self.driver.find_element_by_xpath(self.ads2).click()
        except Exception:
            APP.print_log("Bonus sale adv not found!.")
        APP.progress_bar['value'] += APP.progress_count
        try:
            self.driver.find_element_by_xpath(self.ads3).click()
            APP.print_log("Main adv not is closed.")
        except Exception:
            APP.print_log("Main adv not found!.")
        APP.progress_bar['value'] += APP.progress_count

    def get_data(self):
        username = self.driver.find_element_by_xpath(self.username_xpath).text
        username = username.split(":")[-1][1:]
        credit = self.driver.find_element_by_id(self.user_credit_id).text
        credit = int(credit.replace(".", ''))
        uridium = self.driver.find_element_by_id(self.user_uri_id).text
        uridium = int(uridium.replace(".", ''))
        return {'name': username, 'money': credit, 'money2': uridium}
    
    def click_auction(self):
        self.driver.find_element_by_id(self.auction_id).click()