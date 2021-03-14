import eel
import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
#ініціація eel для графічного інтерфейса
eel.init("interface")
#функція на створення керованого вікна браузера
@eel.expose
def open_api_session(url):
    driver=webdriver.Chrome(executable_path="chromedriver.exe")
    #driver.get("https://e-schools.info/login_")
    driver.get("https://e-schools.info/login?next="+url)
    input("Ввійдіть і натисніть Enter")
    return(driver)
#функція на створення до 4х годин БЕЗ поділу на групи
@eel.expose
def create_hour(driver, date1, number1, date2="", number2="", date3="", number3="", date4="", number4=""):
    driver.find_element(By.NAME, "form-0-date").send_keys(date1)
    driver.find_element(By.NAME, "form-0-number").send_keys(number1)
    if (date2!="" and number2!=""):
        driver.find_element(By.NAME, "form-1-date").send_keys(date2)
        driver.find_element(By.NAME, "form-1-number").send_keys(number2)
        if (date3!="" and number3!=""):
            driver.find_element(By.NAME, "form-2-date").send_keys(date3)
            driver.find_element(By.NAME, "form-2-number").send_keys(number3)
            if (date4!="" and number4!=""):
                driver.find_element(By.NAME, "form-3-date").send_keys(date4)
                driver.find_element(By.NAME, "form-3-number").send_keys(number4)
    driver.execute_script('$(".datepicker").datepicker("hide");')
    driver.find_element(By.CLASS_NAME,"button_blue").click()
#функція на створення до 4х годин з поділом на групи
@eel.expose
def create_hour_subgroup(driver, date1, number1, subgroup1, date2="", number2="", subgroup2="", date3="", number3="", subgroup3="", date4="", number4="", subgroup4=""):
    driver.find_element(By.NAME, "form-0-date").send_keys(date1)
    driver.find_element(By.NAME, "form-0-number").send_keys(number1)
    Select(driver.find_element(By.NAME, "form-0-subgroup")).select_by_index(int(subgroup1))
    if (date2!="" and number2!="" and subgroup2!=""):
        driver.find_element(By.NAME, "form-1-date").send_keys(date2)
        driver.find_element(By.NAME, "form-1-number").send_keys(number2)
        Select(driver.find_element(By.NAME, "form-0-subgroup")).select_by_index(int(subgroup2))
        if (date3!="" and number3!="" and subgroup3!=""):
            driver.find_element(By.NAME, "form-2-date").send_keys(date3)
            driver.find_element(By.NAME, "form-2-number").send_keys(number3)
            Select(driver.find_element(By.NAME, "form-0-subgroup")).select_by_index(int(subgroup3))
            if (date4!="" and number4!="" and subgroup4!=""):
                driver.find_element(By.NAME, "form-3-date").send_keys(date4)
                driver.find_element(By.NAME, "form-3-number").send_keys(number4)
                Select(driver.find_element(By.NAME, "form-0-subgroup")).select_by_index(int(subgroup4))
    driver.execute_script('$(".datepicker").datepicker("hide");')
    driver.find_element(By.CLASS_NAME,"button_blue").click()
@eel.expose
def submit_data(url, subgroups, start_date, end_date, start_week, data, holidays):
    driver=open_api_session(url)
    print(url) #https://demo.e-schools.info/class/8/lessons/100136/add
    print(subgroups) #0
    print(start_date) #2021-03-07
    print(end_date) #2021-03-20
    print(start_week) #1
    print(json.dumps(data)) #[{"week": "1", "day": "3", "lesson": "5"}, {"week": "1", "day": "3", "lesson": "6"}, {"week": "2", "day": "3", "lesson": "5"}, {"week": "2", "day": "3", "lesson": "6"}, {"week": "2", "day": "4", "lesson": "5"}, {"week": "2", "day": "4", "lesson": "6"}]
    hours=[]
    end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d")
    for rule in data:
        now_date=datetime.datetime.strptime(start_date, "%Y-%m-%d")
        now_week=int(start_week)
        if now_week!=int(rule['week']):
            now_date=now_date+datetime.timedelta(days=7-now_date.weekday())
            now_week=int(rule['week'])
        if now_date.weekday()<int(rule['day']):
            now_date=now_date+datetime.timedelta(days=int(rule['day'])-now_date.weekday())
        elif now_date.weekday()>int(rule['day']):
            now_date=now_date+datetime.timedelta(days=14+int(rule['day'])-now_date.weekday())
        while(now_date<=end_date):
            for holiday in holidays:
                start=datetime.datetime.strptime(holiday['start_date'], "%Y-%m-%d")
                end=datetime.datetime.strptime(holiday['end_date'], "%Y-%m-%d")
                if start<=now_date and now_date<=end:
                    now_date=now_date+datetime.timedelta(days=14)
                    print("HOLIDAY")
                    continue
            print(now_date)
            if subgroups=="0":
                hours.append({"date":now_date.strftime("%d.%m.%Y"), "lesson":rule["lesson"]})
                if len(hours)==4:
                    create_hour(driver, hours[0]['date'], hours[0]['lesson'], hours[1]['date'], hours[1]['lesson'], hours[2]['date'], hours[2]['lesson'], hours[3]['date'], hours[3]['lesson'])
                    hours=[]
            else:
                hours.append({"date":now_date.strftime("%d.%m.%Y"), "lesson":rule["lesson"], "subgroup":rule["subgroup"]})
                if len(hours)==4:
                    create_hour_subgroup(driver, hours[0]['date'], hours[0]['lesson'], hours[0]['subgroup'], hours[1]['date'], hours[1]['lesson'], hours[1]['subgroup'], hours[2]['date'], hours[2]['lesson'], hours[2]['subgroup'], hours[3]['date'], hours[3]['lesson'], hours[3]['subgroup'])
                    hours=[]
            now_date=now_date+datetime.timedelta(days=14)
    if len(hours)==1:
        if subgroups=="0":
            create_hour(driver, hours[0]['date'], hours[0]['lesson'])
        else:
            create_hour_subgroup(driver, hours[0]['date'], hours[0]['lesson'], hours[0]['subgroup'])
    elif len(hours)==2:
        if subgroups=="0":
            create_hour(driver, hours[0]['date'], hours[0]['lesson'], hours[1]['date'], hours[1]['lesson'])
        else:
            create_hour_subgroup(driver, hours[0]['date'], hours[0]['lesson'], hours[0]['subgroup'], hours[1]['date'], hours[1]['lesson'], hours[1]['subgroup'])
    elif len(hours)==3:
        if subgroups=="0":
            create_hour(driver, hours[0]['date'], hours[0]['lesson'], hours[1]['date'], hours[1]['lesson'], hours[2]['date'], hours[2]['lesson'])
        else:
            create_hour_subgroup(driver, hours[0]['date'], hours[0]['lesson'], hours[0]['subgroup'], hours[1]['date'], hours[1]['lesson'], hours[1]['subgroup'], hours[2]['date'], hours[2]['lesson'], hours[2]['subgroup'])
    print(u"— Альф, як ти думаєш вирішити проблему бездомних?\n— Уже вирішив!\n— Як вирішив?\n— Для кожного з них будується будинок.\n— А що ти думаєш робити з безробіттям?\n— Його вже немає. Всі будують будинки!\n— Може і воєн більше немає?\n— А кому воювати? Всі бігають, шпалери для нових будинків вибирають.")
#запуск графіки
eel.start("main.html")