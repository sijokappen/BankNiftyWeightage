# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import time
import pandas as pd
import numpy as np


class SeleniumNse(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(30)
        self.base_url = "https://www.nseindia.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_selenium_nse(self):
        driver = self.driver
        driver.get(self.base_url + "/live_market/dynaContent/live_watch/equities_stock_watch.htm?cat=B")
        html_source = driver.page_source
        scrips = []
        for i in range(3, 15):
            print(i)
            elem = driver.find_element_by_xpath("//table[@id='dataTable']/tbody/tr[{}]/td/a".format(i))
            print(elem.get_attribute("href"))
            scrips.append(elem.get_attribute("href"))
        j = 1
        stocks = []
        ffMarCap = []
        price = []
        sum = 0
        for scrip in scrips:
            print(j)
            print(scrip)
            driver.get(scrip)
            print(driver)
            element_1 = driver.find_element_by_xpath('//*[@id="symbol"]')
            print(element_1.get_attribute("innerHTML"))
            stocks.append(element_1.get_attribute("innerHTML"))
            element = driver.find_element_by_xpath("//*[@id=\"ffmid\"]")
            print(element.get_attribute("innerHTML"))
            ffMarCap.append(element.get_attribute("innerHTML").replace(',', ''))
            if (element.get_attribute("innerHTML").replace(',', '')):
                sum += float(element.get_attribute("innerHTML").replace(',', ''))
            element2 = driver.find_element_by_xpath("//*[@id=\"lastPrice\"]")
            print(element2.get_attribute("innerHTML"))
            price.append(element2.get_attribute("innerHTML").replace(',', ''))
            j += 1
            # driver.back()

        weightage = []
        floatingShares = []
        for k in range(0, len(ffMarCap)):
            #weightage_1 = float(ffMarCap[k].replace(',', '')) / float(price[k].replace(',', ''))
            weightage_1 = float(ffMarCap[k].replace(',', ''))/sum*100
            print(stocks[k])
            print(weightage_1)
            weightage.append(weightage_1)
            floatingShares.append(float(ffMarCap[k].replace(',', ''))/float(price[k].replace(',', '')))
        #df = pd.DataFrame({'MarketCap_FF': ffMarCap, 'stocks': stocks, 'weightage': weightage, 'price': price})
        df = pd.DataFrame({'MarketCap_FF': ffMarCap,'floatingShares':floatingShares,'price': price,'stocks': stocks,'weightage': weightage})
        df.tail(10)
        df.to_csv("BankNifty.csv")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
