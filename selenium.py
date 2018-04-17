#!/usr/bin/env python
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import threading


class ThreadFlashops(threading.Thread):

    def __init__(self, ip, is_keep=True):
        threading.Thread.__init__(self)
        self.ip = ip
        self.url = "http://" + ip + "/cgi-bin/luci"
    # BIN = '/tftproot/bin/MU-NF-2018-03-16.bin'
        self.BIN = os.getcwd() + '/op.bin'
        self.IS_KEEP = is_keep

    def login(self):
        user = "root"
        pwd = "nexfi"
        self.driver.get(self.url)
        # assert "Facebook" in driver.title
        elem = self.driver.find_element_by_name("luci_username")
        elem.clear()
        elem.send_keys(user)

        elem = self.driver.find_element_by_name("luci_password")
        elem.clear()
        elem.send_keys(pwd)

        elem.send_keys(Keys.RETURN)

    def flashops(self):
        self.driver.get(self.url)
    #    driver.current_window_handle
        try:
            elem = self.driver.find_element_by_id('keep')
            while self.IS_KEEP != elem.is_selected():
                elem.click()
        except:
            print('exception pass')

        elem = self.driver.find_element_by_id('image')
        elem.send_keys(self.BIN)

        # there is more submit len(elem) == 4
        elem = self.driver.find_elements_by_xpath("//*[@type='submit']")
        elem[-1].click()

        # len(el) == 2
        while len(elem) != 2:
            time.sleep(2)
            elem = self.driver.find_elements_by_xpath("//*[@type='submit']")

        elem[-1].click()

    def save_code(self):
        active_url = self.driver.current_url + '/admin/system/active'
        self.driver.get(active_url)
        elem = self.driver.find_elements_by_id('cbid.mesh.reg.key')
        print('{}: {}'.format(self.ip, elem.value))

    def run(self):
        self.driver = webdriver.Firefox()
        self.login()

        while 'stok' not in self.driver.current_url:
            time.sleep(1)

        if not self.IS_KEEP:
            self.save_code()

#        self.url = self.driver.current_url + '/admin/system/flashops'
#
#        self.flashops()
    #    driver.close()

if __name__ == '__main__':
    ThreadFlashops('192.168.104.4', is_keep=False).start()
    time.sleep(10)
    ThreadFlashops('192.168.104.2', is_keep=False).start()
