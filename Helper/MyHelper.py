from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from datetime import datetime
import config as conf, re, time
from pynput.keyboard import Controller

class MyHelper:

    def do(self):
        self.openShopee()

    def openShopee(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=D:\Chrome\Profile")
        driver = webdriver.Chrome(conf.CHROMEDRIVERPATH, options=options)
        self.goToLoginAndMaximaze(driver)
    
    def goToLoginAndMaximaze(self,driver):
        driver.get("https://shopee.co.id/buyer/login?next=https%3A%2F%2Fshopee.co.id%2F")
        driver.maximize_window()
        driver.get("https://shopee.co.id/buyer/login/qr?next=https%3A%2F%2Fshopee.co.id%2F")

        link_barang = False
        while link_barang == False:
            current_url = driver.current_url
            url_login = re.search("^https://shopee.co.id/buyer/login", current_url)
            if url_login is None:

                self.checkFlashSaleTime(conf.DATETIME_FLASHSALE)
                self.goToUrlProduk(driver, conf.URL_PRODUK)

                self.clickAdditionalOption(driver,conf.ADDITIONAL_VALUE)

                self.clickBeliSekarang(driver)
                cart_pages = False
                print("Prepare cart")
                while cart_pages == False:
                    cart_url = driver.current_url
                    cart_url_is_match = re.search("^https://shopee.co.id/cart", cart_url)
                    if cart_url_is_match:
                        self.clickCheckOut(driver)
                        cart_pages = True
                        break

                self.clickBuatPesanan(driver)

                self.clickBayar(driver)
                self.insertPin(driver, conf.PINSHOPEEPAY)
                self.clickKonfirmasi(driver)

                time.sleep(10000)
                print(driver.current_url)
                link_barang == True
                break


    def checkFlashSaleTime(self,DATETIME_FLASHSALE):
        CHECKOUT_NOW = False
        while CHECKOUT_NOW == False:
            today = datetime.today()
            if today.strftime('%Y-%m-%d %H:%M:%S') == DATETIME_FLASHSALE:
                CHECKOUT_NOW = True
                break

    def goToUrlProduk(self,driver, URL_PRODUK):
        driver.get(URL_PRODUK)
        print("Start Checkout")

    def clickBeliSekarang(self, driver):
        try:
            print("Loading Content Detail Barang")
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'beli sekarang')]")))
            try:
                print("Trying Click Beli Sekarang")
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'beli sekarang')]"))).click()
            except ElementClickInterceptedException:
                print("Button Cannot Be Clicked")
                self.clickBeliSekarang(driver)
        except TimeoutException:
            print("Failed To Load Content Detail Barang")        
            self.clickBeliSekarang(driver)

    def clickCheckOut(self,driver):
        print("Cart Available")
        try:
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'checkout')]")))
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'checkout')]"))).click()
            except ElementClickInterceptedException:
                self.clickCheckOut(driver)
        except TimeoutException:
            self.clickCheckOut(driver)
        print("Moving To Checkout cart Page")

    def clickBuatPesanan(self,driver):
        print("On Check Out Page")
        try:
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Buat Pesanan')]")))
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Buat Pesanan')]"))).click()
            except ElementClickInterceptedException:
                print("Button Buat Pesanan is still not click able")
                self.clickBuatPesanan(driver)
        except TimeoutException:
            print("Try to reload checkout page")        
            self.clickBuatPesanan(driver)
        print("Check Out Done")

    def clickBayar(self,driver):
        print("Bayar ShopeePay")
        try:
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, "pay-button")))
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "pay-button"))).click()
            except ElementClickInterceptedException:
                print("Button Bayar is still not click able")
                self.clickBayar(driver)
        except TimeoutException:
            print("Try to reload bayar page")        
            self.clickBayar(driver)
        print("Bayar Done")

    def insertPin(self,driver, pin):
        print("Memasukan PIN")
        for mypin in pin:
            self.setPinNumber(driver, mypin)
        print("Memasukan PIN Selesai")

    def setPinNumber(self,driver, mypin):
        print("Set PIN :")
        print(mypin)
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='digit-input active']")))
            keyboard = Controller()
            keyboard.press(mypin)
            keyboard.release(mypin)
        except TimeoutException:
            print("Try set pin")
            self.setPinNumber(driver)

    def clickKonfirmasi(self,driver):
        print("Klik konfirmasi")
        try:
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='okText']")))
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='okText']"))).click()
            except ElementClickInterceptedException:
                print("Button konfirmasi is still not click able")
                self.clickKonfirmasi(driver)
        except TimeoutException:
            print("Try to reload konfirmasi page")
            self.clickKonfirmasi(driver)
        print("Konfirmasi done")

    def clickAdditionalOption(self,driver,value):
        for add in value:            
            print("Click " + add)
            try:
                WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., '"+ add +"')]")))
                try:
                    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '"+ add +"')]"))).click()
                except ElementClickInterceptedException:
                    self.clickAdditionalOption(driver)
            except TimeoutException:
                self.clickAdditionalOption(driver)
            print(add + " Clicked")
