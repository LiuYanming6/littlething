#!/usr/bin/env python
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import threading
import argparse

"""
根据选择的浏览器选择对应的driver
http://selenium-python.readthedocs.io/installation.html
"""


class ThreadFlashops(threading.Thread):

    def __init__(self, ip, is_keep=True, pwd='nexfi'):
        threading.Thread.__init__(self)
        self.ip = ip
        if ip == '192.168.2.2':
            pwd = 'admin'
        self.url = "http://" + ip + "/cgi-bin/luci"
    # BIN = '/tftproot/bin/MU-NF-2018-03-16.bin'
        self.BIN = os.getcwd() + '/op.bin'
        self.IS_KEEP = not not is_keep
        self.pwd = pwd

    def login(self):
        user = "root"
        self.driver.get(self.url)
        # assert "Facebook" in driver.title
        elem = self.driver.find_element_by_name("luci_username")
        elem.clear()
        elem.send_keys(user)

        elem = self.driver.find_element_by_name("luci_password")
        elem.clear()
        elem.send_keys(self.pwd)

        elem.send_keys(Keys.RETURN)

    def flashops(self):
        self.driver.get(self.url)
    #    driver.current_window_handle
        try:
            elem = self.driver.find_element_by_id('keep')
            while self.IS_KEEP != elem.is_selected():
                print(self.IS_KEEP, elem.is_selected())
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
        """
        to fix
        """
        active_url = self.driver.current_url + '/admin/system/active'
        self.driver.get(active_url)
        elem = self.driver.find_elements_by_id('cbid.mesh.reg.key')
        print('{}: {}'.format(self.ip, elem.value))

    def run(self):
        self.driver = webdriver.Firefox()
        self.login()

        time.sleep(3)
        print(self.ip)
        while 'stok' not in self.driver.current_url and self.ip != '192.168.2.2':
            time.sleep(1)

        if not self.IS_KEEP:
            self.save_code()

        self.url = self.driver.current_url + '/admin/system/flashops'

        self.flashops()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='-------------------------------',
                                     epilog="-------------------------------")
    parser.add_argument('-i', action='store',
                        dest='ip',
                        default='192.168.104.254',
                        help='ip addr')
    parser.add_argument('-k', action='store',
                        dest='keep',
                        default='True',
                        help='config save-1 or not save-0')

    args = parser.parse_args()
    print(args.ip, args.keep)

    ThreadFlashops(args.ip, is_keep=args.keep).start()

