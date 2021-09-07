# import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser =webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    update.message.reply_text('before getting url')
    
    browser.get(url)
#     browser.maximize_window()
    time.sleep(10)
    browser.find_element_by_xpath('//input[@id="autocomplete"]').send_keys(startCity)
    update.message.reply_text('set the startCity')
    time.sleep(1)
    browser.find_element_by_xpath('//label[@for="autocomplete2"]/input').send_keys(endCity)
    update.message.reply_text('set the endCity')
    time.sleep(1)
    browser.find_element_by_xpath('//label[@for="datetimepickerDep"]/input').clear()
    update.message.reply_text('clear')
    time.sleep(1)

    dateAller=browser.find_element_by_xpath('//label[@for="datetimepickerDep"]/input')
    dateAller.send_keys(date+' 00:00')
    update.message.reply_text('set the dateAller')
    time.sleep(1)
    dateAller.send_keys(Keys.RETURN)
    time.sleep(1)
    dateRetour=browser.find_element_by_xpath('//label[@for="datetimepickerArr"]/input')
    dateRetour.send_keys(date+' 00:00')
    time.sleep(1)
    dateRetour.send_keys(Keys.RETURN)
    time.sleep(1)
#     cheek=browser.find_element_by_xpath('//div[@class="form-checkbox font11"]/div[@class="form-item"]/label[@for="radioAller"]')
#     browser.execute_script("arguments[0].click();", cheek)
    update.message.reply_text('choisir Aller simple')
#     cheek.click()
    time.sleep(2)
    button1Page1 = browser.find_element_by_xpath('//form/div[@class="form-item see-all show-on-desktop"]/button')
#     input.send_keys(Keys.RETURN)
    update.message.reply_text('search the button1Page1')
    browser.execute_script("arguments[0].click();", button1Page1)
#     button1Page1.send_keys(Keys.RETURN) 
#     script = "window.scrollTo(0,document.body.scrollHeight)"
#     browser.execute_script(script)
    time.sleep(5)
#     button1Page1 = browser.find_element_by_xpath('//div[@class="form-item see-all show-on-desktop"]/button')
 
#     button1Page1 = browser.find_element_by_xpath('//button[@type="submit"]')
    
    
#     wait=WebDriverWait(browser, 20)
#     button=wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@type="submit"]')))
#     button.click()
#     button1Page1.click()
    
    update.message.reply_text('click the button1Page1')
    time.sleep(10)
    button2Page1 = browser.find_element_by_xpath('//tr/td[6]/a')
    update.message.reply_text('search the button2Page1')
    button2Page1.click()
    update.message.reply_text('click the button2Page1')
    time.sleep(15)
#     browser.maximize_window()
    update.message.reply_text(browser.title)
    newURl = browser.window_handles[1]
    browser.switch_to.window(newURl)
    time.sleep(3)
    update.message.reply_text(browser.title)
#     script = "window.scrollTo(0,600)"
#     browser.execute_script("window.scrollTo(0,600)";)
    scroll=browser.find_element_by_tag_name('html')
    scroll.send_keys(Keys.PAGE_DOWN)
#     browser.save_screenshot("screenshot.png")
    update.message.reply_text(os.getcwd())
    update.message.bot.send_photo(chat_id=update.effective_chat.id, photo=open(browser.current_url, 'rb'))
#     scroll.send_keys(Keys.PAGE_DOWN)
#     scroll.send_keys(Keys.PAGE_DOWN)
#     scroll.send_keys(Keys.PAGE_DOWN)
#     scroll.send_keys(Keys.PAGE_DOWN)
#     scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(5)
    
    button = browser.find_element_by_xpath("//div[@class='searchForm_footer  ']/div[@class='searchForm_footer--right']/button")
    update.message.reply_text('search the button search')
    browser.execute_script("arguments[0].click();", button)
#     button.click()
    update.message.reply_text('click the button search')
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
