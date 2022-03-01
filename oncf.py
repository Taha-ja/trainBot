# import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# import requests
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
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
cityDict={
	'ADAKHLA':796,
	'AEROPORT MED V':190,
	'FES':380,
	'OUJDA':490,
	'KENITRA':250,
	'TAZA':431,
	'OUED AMLIL':423,
}
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.experimental_options["prefs"] = { 
	"profile.managed_default_content_settings.images": 2, 
	"profile.managed_default_content_settings.stylesheets": 2, 
	"profile.managed_default_content_settings.javascript": 2, 
	"profile.managed_default_content_settings.cookies": 2, 
	"profile.managed_default_content_settings.geolocation": 2, 
	"profile.default_content_setting_values.notifications": 2, 
    }
    url = f'https://www.oncf.ma/fr/Horaires'
    
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument("disable-infobars")
#     chrome_options.add_argument("--disable-extensions")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser =webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    time.sleep(5)
    t=int(time.time())-((datetime.datetime.now().time().hour)*3600+datetime.datetime.now().time().minute*60+datetime.datetime.now().time().second)
    Day=int(date[:2]);Month=int(date[3:5]);Year=int(date[6:])
    dateA=datetime.datetime(Year,Month,Day)
    dateNow=datetime.datetime.now()
    dateToday=datetime.datetime(dateNow.year,dateNow.month,dateNow.day)
    nbJ=(dateA-dateToday).days
    url = f'https://www.oncf-voyages.ma/recherche-disponibilites/{cityDict[startCity]}/{cityDict[endCity]}/{t+86400*nbJ}'
    #url="https://www.oncf-voyages.ma/recherche-disponibilites"	
    browser.get(url)
    time.sleep(4)
    browser.implicitly_wait(10)
    browser.save_screenshot("screenshot1.png")
    update.message.bot.send_photo(chat_id=update.effective_chat.id, photo=open('/app/screenshot1.png', 'rb'))	
#     scroll=browser.find_element_by_tag_name('html')
#     scroll.send_keys(Keys.PAGE_DOWN)
#     button = browser.find_element_by_xpath("//div[@class='searchForm_footer  ']/div[@class='searchForm_footer--right']/button")
#     browser.execute_script("arguments[0].click();", button)
#     update.message.reply_text('click the button search')
#     browser.implicitly_wait(10)
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
