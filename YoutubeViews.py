from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox
#from PyQt5.QtGui import QDoubleValidator, QValidator

class AppDemo(QLineEdit):
    def __init__(self):
        super().__init__()
        self.list_errors = []
        self.list_text = []
        self.urls = 'https://rifinder.com'
        self.repeat = 1
        self.watchtime = 1
        self.next_part = None
        self.resize(700,60)
        self.setStyleSheet('font-size: 25px')
        self.editingFinished.connect(self.validating)
        #self.browser_setup()

    def browser_setup(self):
        self.profile=webdriver.FirefoxProfile()
        self.profile.set_preference('network.proxy.type', 1)
        self.profile.set_preference('network.proxy.socks', '127.0.0.1')
        self.profile.set_preference('network.proxy.socks_port', 9150)
        self.browser=webdriver.Firefox(self.profile)

    def validating(self):
        #print(self.text())
        if 'https' not in self.text():
            if self.text() not in self.list_errors:
                self.list_errors.append(self.text())
                #print("Fasle")
                self.show_popup()

        elif 'https' in self.text():
            if self.text() not in self.list_text:
                self.list_text.append(self.text())
                for i in range(len(self.text())):
                    if self.text()[i] == ' ':
                        temp = i
                        break
                self.urls = self.text()[:temp]
                self.next_part = self.text()[temp+1:]
                #print(self.next_part)
                temp2 = None
                for j in range(len(self.next_part)):
                    if self.next_part[j] == '-':
                        temp2 = j
                        break
                if temp2!=None:
                    self.repeat = self.next_part[:temp2]
                    self.watchtime = self.next_part[temp2+1:]
                    print("---Video URL = {} --- \n---No of Repeatation = {} --- \n---Watchtime in Seconds = {} ---".format(self.urls, self.repeat, self.watchtime))
                    self.play_video()
                else:
                    self.show_popup()

                #self.play_video()

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("URL Not Valid")
        msg.setText("Your Input is Not Valid. Please enter a valid URL")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry)
        x = msg.exec_()

    def play_video(self):
        #for url in self.urls:
         #   for repeat in range(self.repeat):
          #      self.browser.get('url')
        self.browser_setup()
        self.browser.get("https://www.youtube.com/")
        try:
            no_thanks = self.browser.find_element_by_xpath("/html/body/ytd-app/ytd-popup-container/paper-dialog/yt-upsell-dialog-renderer/div/div[3]/div[1]/yt-button-renderer/a")
        except:
            no_thanks = None
            print("...No need to Sign In...")
        sleep(20)
        if no_thanks != None:
            no_thanks.click()
            sleep(25)
            try:
                print("\n Searching the 'I Agree' Button")
                agree = self.browser.find_element_by_xpath("/html/body/div/c-wiz/div[2]/div/div/div/div/div[2]/form/div/span/span")
                #/html/body/div/c-wiz/div[2]/div/div/div/div/div[2]/form/div/span/span
                print("agreed")
                agree.click()
            except:
                print("\n Click the 'I agree' Button Manually. Bot is not able to find it. You have 30 seconds to do it.\n")
                agree = None
                sleep(30)
            sleep(10)
        #sleep(10)
        print("REPEATATION STARTING")
        #print(self.repeat)
        for i in range(int(self.repeat)):
            self.browser.get(self.urls)
            #print(self.repeat, self.urls)
            print("Repeat No : {}".format(i+1))
            sleep(15)
            try:
                play = self.browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[27]/div[2]/div[1]/span[2]/button')
                play.click()
            except:
                print("...Fix Captcha and Rerun this Program...")
            sleep(int(self.watchtime))
            self.browser.refresh()

        self.browser.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = AppDemo()
    ui.show()
    sys.exit(app.exec_())