from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from subprocess import CREATE_NO_WINDOW
from webdriver_manager.chrome import ChromeDriverManager
from Scrape.Pages.loginPage import LoginPage
from Scrape.Pages.homePage import HomePage
from Scrape.Pages.auctionPage import AuctionPage
import Scrape.constants as c
import os, time

class ScrapeAuction:

    @classmethod
    def setUpClass(cls, APP):
        options = webdriver.ChromeOptions()
        options.headless = bool(APP.headless_valid.get())
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        # service.creationflags = CREATE_NO_WINDOW
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.implicitly_wait(10)
    
    def run_scrape(self, username, password, lst, APP):
        driver = self.driver

        driver.get("https://www.darkorbit.com/")
        login = LoginPage(driver)
        login.enter_data(username, password, APP)
        APP.progress_bar['value'] += APP.progress_count
        try:
            APP.print_log("Logging to: "+username)
            APP.progress_bar['value'] += APP.progress_count
        except Exception:
            pass
        login.save_exit_panel() # THIS IS NOT WORKING
        return
        login.click_login()
        APP.progress_bar['value'] += APP.progress_count

        homepage = HomePage(driver)
        try:
            APP.print_log("Closing all expected advertisements.")
            APP.progress_bar['value'] += APP.progress_count
        except Exception:
            pass
        homepage.close_ads(APP)
        user_data = homepage.get_data()
        APP.progress_bar['value'] += APP.progress_count
        try:
            APP.print_log("Advancing to the auction page.")
        except Exception:
            pass
        homepage.click_auction()
        APP.progress_bar['value'] += APP.progress_count

        auction = AuctionPage(driver)
        APP.progress_bar['value'] += APP.progress_count
        try:
            APP.print_log("Getting all information and items.")
        except Exception:
            pass
        deadline, data = auction.get_items_data(lst, APP)
        user_data['deadline'] = deadline
        APP.progress_bar['value'] += APP.progress_count

        return user_data, data
        

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()