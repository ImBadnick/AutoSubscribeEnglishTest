from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display 
import time
from signal import signal, SIGINT
from sys import exit
from webdriver_manager.chrome import ChromeDriverManager


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
        self.driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=chrome_options)
        print("Opening Web Window")
        self.driver.get('https://elearning.cli.unipi.it/')
        
    def Subscribe(self):
        self.driver.get('https://elearning.cli.unipi.it/course/view.php?id=2044') #link
        self.login() # Login
        try:
            self.driver.find_element_by_xpath('//li[@class="activity reservation modtype_reservation "]//a').click() #Click on calendar icon
        except NoSuchElementException:
            print("Inserted wrong email/password!")
            return
        
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
            
        except NoSuchElementException:
            print("Already Logged In!")


    def quitDriver(self):
        print("Quit")
        self.driver.quit()
        try: 
            self.display.stop()
        except Exception:
            pass

    def handler(self,signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        self.driver.quit()
        try: 
            self.display.stop()
        except Exception:
            pass
        exit(0)

if __name__ == '__main__':
    scraper = Scraper()  # Scraper object
    print("Logged In")
    scraper.Subscribe()  # Starting scraper
    scraper.quitDriver()
    
