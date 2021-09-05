# import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import requests
# from selenium.webdriver.common.action_chains import ActionChains
import time, datetime
# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)






# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
token='1968918139:AAGaQT5BLUWxhu_9CS1Owkddh1NwZU2e_QA'
# chatId=1145262131
updater=Updater(token=token)
disp=updater.dispatcher

# questions=['quelle est votre ville de d\'arrivée?',"merci de saisir la date de départ"]

var=[]
quest=[] 
def start(update,context):
    var.clear()
    quest.clear()
    quest.append('quelle est votre ville de d\'arrivée?')
    quest.append("merci de saisir la date de départ")
    update.message.reply_text('welcom in our bot')
    update.message.reply_text('quelle est votre ville de départ?')
def msg(update,context):
    var.append(update.message.text)
    if quest!=[]:
        update.message.reply_text(quest[0])
        quest.pop(0)
def search(update,context):
    startCity = var[0].upper()
    endCity = var[1].upper()
    date = var[2]
    url = f'https://www.oncf.ma/fr/Horaires'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser =webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    update.message.reply_text('before getting url')
    
    browser.get(url)
    browser.maximize_window()
    browser.implicitly_wait(5)
    browser.find_element_by_xpath('//input[@id="autocomplete"]').send_keys(startCity)
    time.sleep(1)
    browser.find_element_by_xpath('//label[@for="autocomplete2"]/input').send_keys(endCity)
    time.sleep(1)
    browser.find_element_by_xpath('//label[@for="datetimepickerDep"]/input').clear()
    time.sleep(1)
    browser.find_element_by_xpath('//label[@for="datetimepickerDep"]/input').send_keys(date+' 00:00')
    time.sleep(1)
    browser.find_element_by_xpath('//label[@for="datetimepickerArr"]/input').send_keys(date+' 00:00')
    time.sleep(10)
  
    button1Page1 = browser.find_element_by_xpath('//div[@class="form-item see-all show-on-desktop"]/button')
    button1Page1.click()
    time.sleep(10)
    button2Page1 = browser.find_element_by_xpath('//tr/td[6]/a')
    button2Page1.click()
    time.sleep(15)
    browser.maximize_window()
    newURl = browser.window_handles[1]
    browser.switch_to.window(newURl)
    script = "window.scrollTo(0,600)"
    browser.execute_script(script)
    time.sleep(5)

    button = browser.find_element_by_xpath("//div[@class='searchForm_footer--right']/button")
    button.click()
    browser.implicitly_wait(10)
    time.sleep(5)

    depart = []
    arrive = []
    prix_ticket = []


    def getInformation():
        price = browser.find_elements_by_xpath('//label[@class="price"]')
        temps = browser.find_elements_by_xpath('//label[@class="date"]')
        for i in range(len(temps)):
            if i % 2 == 0:
                depart.append(temps[i].text)
            else:
                arrive.append(temps[i].text)
        for prix in price:
            prix_ticket.append(int(prix.text[:-3]))

    rsp = True
    while rsp:
        
        # script = "window.scrollTo(0,document.body.scrollHeight)"
        # browser.execute_script(script)
        getInformation()
        time.sleep(2)
        try:
            next = browser.find_element_by_xpath('//div[@class="ant-card-body"]/a[@tag="a"]')
            next.click()
        except:
            print("End of results!!")
            rsp = False
    
    ultimitInfo = zip(depart, arrive, prix_ticket)
    print(ultimitInfo)

    def results():
        Str = f'les trains de {date} est:\n'
        for info in ultimitInfo:
            # if info[2]==min(prix_ticket):
                Str += f"De:{info[0]} à:{info[1]} prix:{info[2]} \n"
        return Str
    update.message.reply_text(results())
    browser.quit()
    
start_handler=CommandHandler('start',start)
simple=MessageHandler(Filters.text,msg)
disp.add_handler(CommandHandler('search',search))
disp.add_handler(start_handler)
disp.add_handler(simple)
updater.start_polling()
updater.idle()
