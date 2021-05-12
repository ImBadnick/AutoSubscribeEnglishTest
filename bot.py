from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from signal import signal, SIGINT
from sys import exit
import sys
import os
import pickle



class Scraper:
    def __init__(self):
        signal(SIGINT,self.handler)
        self.username = 'username'
        self.password = 'password'
        #Driver setup
        # self.display = Display(visible=0, size=(800,600))
        # self.display.start()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-data-dir=~/Library/Application Support/Google/Chrome/Default/Cookies")
        self.driver = webdriver.Chrome("/home/badnick/Scrivania/Github/BotInstagram/SocialMoney/chromedriver", options=chrome_options)
        print("Opening Web Window")
        self.driver.get('https://elearning.cli.unipi.it/')
        self.load_cookies()
        
    def scrapeImages(self):
        self.driver.get('https://elearning.cli.unipi.it/course/view.php?id=2044') #link
        self.login() # Login
        self.driver.find_element_by_xpath('//img[@src="https://elearning.cli.unipi.it/theme/image.php/boost/reservation/1616951889/icon"]').click() #Click on calendar icon
        
        direction = "right" ; NotDone = True
        
        while NotDone:
            try:
                self.driver.find_element_by_xpath('//input[@name="reserve"]').click()
                self.login() # Login in case session as expired
                NotDone = False

            except NoSuchElementException:
                try:
                    if direction == "right":
                        self.driver.find_element_by_xpath('//div[@class="float-right"]').click()
                    else:
                        self.driver.find_element_by_xpath('//div[@class="float-left"]').click()
                    time.sleep(1)
                except Exception:
                    direction = "right" if direction == 'left' else 'left' #Change click direction
                    self.login() # Login in case session as expired
                    time.sleep(60)

    def login(self):
        try:
            self.driver.find_elements_by_xpath('//div[@class="card"]//span[@style="text-decoration:underline;"]')[0].click()
            username = self.driver.find_element_by_xpath('//input[@id="username"]')    
            password = self.driver.find_element_by_xpath('//input[@id="password"]')
            username.send_keys(self.username) ; password.send_keys(self.password)
            self.driver.find_element_by_xpath('//button[@class="form-element form-button"]').click()
            
        except Exception:
            print("Already Logged In!")


    def quitDriver(self):
        print("Quit")
        self.save_cookies()
        self.driver.quit()
        try: 
            self.display.stop()
        except Exception:
            pass

    def handler(self,signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        self.driver.quit()
        self.display.stop()
        exit(0)

    def load_cookies(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except Exception:
            print("Failed to load cookies")

    def save_cookies(self):
        pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))

scraper = Scraper()  # Scraper object
print("Logged In")
scraper.scrapeImages()  # Starting scraper
scraper.quitDriver()
