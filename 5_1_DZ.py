from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint

# БЛОК MongoDB
client = MongoClient('127.0.0.1', 27017)
db5 = client['mailru']
mails_parse = db5.mailru
mails_parse.delete_many({})

# Функц записи в базу новости
def record_mails(from_who, when, head_name, body_text):
    mails_parse.insert_one({'from_who': from_who, 'when': when, 'head_name': head_name,'body_text': body_text})

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')


login = driver.find_element_by_name('login')
login.send_keys('study.ai_172@mail.ru')

# альтернативный ящик где меньше писем
#login.send_keys('test_gb_05@mail.ru')

button_passw = driver.find_element_by_xpath("//button[@class = 'button svelte-no02r']")
button_passw.click()
time.sleep(3)

passwd = driver.find_element_by_name('password')
passwd.send_keys('NextPassword172')

# альтернативный ящик где меньше писем
#passwd.send_keys('laguna321')

button_enter = driver.find_element_by_xpath("//button[@class = 'second-button svelte-no02r']")
button_enter.click()

time.sleep(5)
href_items = []

mails = driver.find_elements_by_class_name('dataset__items')
time.sleep(3)

mailss = driver.find_element_by_xpath("//a[@class = 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal']")
driver.get(mailss.get_attribute('href'))
m = 1
mail_text = 1
mail_date = 1
mail_url = 1
time.sleep(2)
while driver.current_url != mail_url:

        time.sleep(2)
        # отладка
        #m = driver.find_elements_by_xpath("//span[contains(@class, 'disabled')]")
        #pprint(driver.find_elements_by_xpath("//span[contains(@class, 'disabled')]"))
        mail_from_block = driver.find_element_by_class_name('letter-contact')
        mail_from = (mail_from_block.get_attribute('title'))
        mail_date = driver.find_element_by_class_name('letter__date').text
        mail_name = driver.find_element_by_class_name('thread__subject').text
        mail_text = driver.find_element_by_class_name('html-expander').text
        mail_url = driver.current_url
        # отладка
        #print(mail_url)
        #print(mail_from, mail_date, mail_name, mail_text)
        time.sleep(1)
        m = driver.find_elements_by_xpath("//span[contains(@class, 'disabled')]")
        record_mails(mail_from, mail_date, mail_name, mail_text)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.ARROW_DOWN).key_up(Keys.CONTROL).key_up(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(1)

# ПРОВЕРИМ БАЗУ

for el in db5.mailru.find({}):
    pprint(el)




