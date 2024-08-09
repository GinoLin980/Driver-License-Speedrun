from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from apscheduler.schedulers.blocking import BlockingScheduler
import random, time, re, toml, os, sys
import requests
import datetime
from datetime import timedelta
from dateutil import parser
from ask_users_options import ask_users_options

if not os.path.exists("msedgedriver.exe"):
    print("請下載Microsoft Edge Webdriver並放在與此檔案同目錄")
    input("按Enter 結束...")
    sys.exit()


data = ask_users_options()
imformation = toml.load("imformation.toml")

ID_NUMBER = imformation["ID_NUMBER"]
BIRTH = imformation["BIRTH"]
NAME = imformation["NAME"]
PHONE = imformation["PHONE"]
EMAIL = imformation["EMAIL"]

MVO = data["MVO"]
STATION = data["Station"]
RETAKE = data["Retake"]
KEYWORDS = data["Keywords"]

MOCK = True

def information_validation():
    # Regular expressions
    id_number_regex = r"^[A-Z]\d{9}$"
    birth_regex = r"^[01]\d{2}\d{2}\d{2}$"
    name_regex = r"^[\u4e00-\u9fa5]+$"
    phone_regex = r"^[0][9]\d{8}$"
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    # Validation
    if not  re.match(id_number_regex, ID_NUMBER):
        print(f"無效的身分證字號: {ID_NUMBER}。")
        input("請按Enter繼續...")
        sys.exit()
    if not  re.match(birth_regex, BIRTH):
        print(f"無效的出生日期: {BIRTH} 示範：0940803。")
        input("請按Enter繼續...")
        sys.exit()
    if not  re.match(name_regex, NAME):
        print(f"無效的姓名: {NAME} 請使用中文名。")
        input("請按Enter繼續...")
        sys.exit()
    if not  re.match(phone_regex, PHONE):
        print(f"無效的手機號碼: {PHONE} 示範：09xxxxxxxx。")
        input("請按Enter繼續...")
        sys.exit()
    if not  re.match(email_regex, EMAIL):
        print(f"無效的電子郵件: {EMAIL}。")
        input("請按Enter繼續...")
        sys.exit()

def get_latest_sign_date_in_mingguo():
    # Fetch the current time for Taiwan from worldtimeapi.org
    response = requests.get("http://worldtimeapi.org/api/timezone/Asia/Taipei")
    data = response.json()

    # Extract the datetime string from the response
    datetime_str = data['datetime']

    # Parse the datetime string using dateutil.parser
    taiwan_time = parser.isoparse(datetime_str)

    # Get the current local time and make it offset-aware
    local_time = datetime.datetime.now(datetime.timezone.utc).astimezone(taiwan_time.tzinfo)

    # Calculate the difference in minutes
    time_difference = abs((taiwan_time - local_time).total_seconds() / 60)

    # Allow a 1-minute error margin
    assert time_difference <= 1, f"本地時間錯誤，有{time_difference:.0f}分鐘誤差。"

    # Calculate the date 30 days from now
    future_date = taiwan_time + timedelta(days=30)

    # Format the future date
    formatted_future_date = future_date.strftime("%Y%m%d")
    formatted_future_date_mingguo = str(int(formatted_future_date[:4]) - 1911) + formatted_future_date[4:]

    return formatted_future_date_mingguo


def driver_license_speedrun():
    options = webdriver.EdgeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Edge(options=options)

    driver.get("https://www.mvdis.gov.tw/m3-emv-trn/exm/locations")

    time.sleep(2)

    select_scooter = Select(driver.find_element(By.ID, "licenseTypeCode"))
    select_scooter.select_by_value("3") # 普通重型機車

    date = driver.find_element(By.ID, "expectExamDateStr")
    date.send_keys(get_latest_sign_date_in_mingguo())

    select_placeLv1 = Select(driver.find_element(By.ID, "dmvNoLv1"))
    select_placeLv1.select_by_visible_text(MVO)

    time.sleep(2)

    select_place = Select(driver.find_element(By.ID, "dmvNo"))
    select_place.select_by_visible_text(STATION)

    search_place = driver.find_element(By.PARTIAL_LINK_TEXT, "查詢場次 Search")
    search_place.click()

    select_round = driver.find_element(By.PARTIAL_LINK_TEXT, "選擇場次繼續報名")
    select_round.click()

    # Find tables contain imformation
    try:
        inner_table = driver.find_element(By.ID, "trnTable")
    except:
        print("No Imformation!")
        import sys
        sys.exit()
    # Find all rows in the inner table
    rows = inner_table.find_elements(By.TAG_NAME, "tr")
    rows.pop(0)

    # Iterate through the rows to find the correct one
    for row in rows:
        # Check if it's not for experienced drivers and not full
        if not RETAKE:
            if any(keyword in row.text for keyword in KEYWORDS):
                if "額滿" in row.text:
                    continue
                if "(初考生勿預約本場次)" in row.text:
                    continue
                # Find the sign-up button
                result = (row.text, row.accessible_name)
                signup_button = row.find_element(By.PARTIAL_LINK_TEXT, "報名 SignUp")
                # Click the button
                signup_button.click()
                break
                    
        else:
            if any(keyword in row.text for keyword in KEYWORDS):
                # Find the sign-up button
                if "額滿" in row.text:
                    continue
                try:
                    signup_button = row.find_element(By.PARTIAL_LINK_TEXT, "報名 SignUp")
                    # Click the button
                    signup_button.click()
                    break
                except:
                    print("沒有重考名額!")
                    import sys
                    sys.exit()

    accept_terms = driver.find_element(By.PARTIAL_LINK_TEXT, "我已充分知悉相關約定並願接受")
    accept_terms.click()

    ID_input = driver.find_element(By.ID, "idNo")
    ID_input.send_keys(ID_NUMBER)

    birth_input = driver.find_element(By.ID, "birthdayStr")
    birth_input.send_keys(BIRTH)

    name_input = driver.find_element(By.ID, "name")
    name_input.send_keys(NAME)

    phone_input = driver.find_element(By.ID, "contactTel")
    phone_input.send_keys(PHONE)

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(EMAIL)

    viewport_width = driver.execute_script("return window.innerWidth;")
    viewport_height = driver.execute_script("return window.innerHeight;")

    random_x = random.randint(0, viewport_width - 1)
    random_y = random.randint(0, viewport_height - 1)

    # Perform a random click
    actions = ActionChains(driver)
    actions.move_by_offset(random_x, random_y).click().perform()

    time.sleep(0.6)

    sign_up = driver.find_element(By.PARTIAL_LINK_TEXT, "報名 SignUp")
    sign_up.click()

    print(result)
    with open("result.txt", "w", encoding="utf-8") as f:
        for i in result:
            f.write(i)

if not MOCK:
    information_validation()
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    job = scheduler.add_job(driver_license_speedrun, 'cron', hour=0, minute=0, second=5) # start at 00:00:5
    print("排程成功，城市將在00:00:05自動運行，請勿關閉程式。")
    scheduler.start()
else:
    driver_license_speedrun()