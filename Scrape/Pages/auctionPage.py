from selenium.webdriver.common.action_chains import ActionChains

class AuctionPage:
    
    def __init__(self, driver):
        self.driver = driver
        
        self.deadline_id = 'countdown_hour'

        # items
        self.laserx2   = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[1]/td[{}]'
        self.laserx3   = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[2]/td[{}]'
        self.laserabs  = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[3]/td[{}]'
        self.rocket4k  = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[4]/td[{}]'
        self.rocket6k  = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[5]/td[{}]'
        self.speedgen  = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[7]/td[{}]'
        self.shieldgen = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[8]/td[{}]'
        self.lf3       = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[34]/td[{}]'
        self.iris      = '//*[@id="auction_content_hour"]/div[1]/table/tbody[2]/div/div[1]/tr[38]/td[{}]'

    def get_items_data(self, lst, APP):
        item_lst = [self.laserx2, self.laserx3, self.laserabs, self.rocket4k, self.rocket6k, self.speedgen, self.shieldgen, self.lf3, self.iris]
        choosed_items = [item_lst[i] for i in lst]
        progres_update = round(len(choosed_items)/APP.progress_count)
        
        data = []
        for item, item_id in zip(choosed_items,lst):
            
            move_element = self.driver.find_element_by_xpath(item.format(4))
            action1 = ActionChains(self.driver)
            action1.move_to_element(move_element).perform()
            
            username = move_element.text
            money = self.driver.find_element_by_xpath(item.format(5)).text
            money = int(money.replace('.', ''))

            data.append({"name": username, "money": money, "id": item_id})
            APP.progress_bar['value'] += progres_update

        deadline = self.driver.find_element_by_id(self.deadline_id).text

        return deadline, data