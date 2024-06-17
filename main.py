from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep

## Update USERNAME and PASSWORD to login
USERNAME = "*********"
PASSWORD = "*********"
SECOND_PLAYER = "NAN CHEN"

TIMESLOT = "16:00:00"
# priority for [court1, court2, court3, court4]
# 0 is highest priority
PRIORITY = [3, 2, 1, 0]

# Not in use, TBD
# priority for [6to7, 7to8, 8to9] sessions
PRIORITY = [2, 0, 1]


COURT_RESERVE_PAGE = "https://app.courtreserve.com/Online/Account/Login"

def login(browser):
    username_input = browser.find_element(By.CSS_SELECTOR,'input[id="UserNameOrEmail"]')
    pwd_input = browser.find_element(By.CSS_SELECTOR,'input[id="Password"]')

    username_input.send_keys(USERNAME)
    pwd_input.send_keys(PASSWORD)
    login = browser.find_element(By.CSS_SELECTOR,'button[type="button"]')
    login.click()

# not in use, this is for getting any available slot
def book_a_court(browser):
    browser.maximize_window()
    #lnks=browser.find_elements(By.XPATH, "(//a[contains(@href,'/Reservations/Bookings')])")

    browser.get("https://app.courtreserve.com/Online/Reservations/Bookings/9705?sId=13790")
    date = browser.find_element(By.XPATH,"//span[@class='k-sm-date-format']").get_attribute("innerText")
    cur_date = date
    prev_date = ""
    found_date = False
    while prev_date != cur_date and not found_date:
        next_day_button = browser.find_element(By.XPATH,"//button[@title='Next']")
        sleep(1)
        reserve_8to9 = browser.find_elements(By.XPATH,'//button[(contains(@start, "%s")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]'%str(TIMESLOT))
        #reserve_8to9 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[(contains(@start, "20:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')))

        if len(reserve_8to9) <= 0:
            prev_date = cur_date
            next_day_button.click()
            cur_date = browser.find_element(By.XPATH,"//span[@class='k-sm-date-format']").get_attribute("innerText")
            continue
        
        found_date = True

    if found_date:
        print("Date Found ", cur_date)
    else:
        print("No Availiability")

def book_a_court_at_certain_date(browser, date):
    browser.maximize_window()
    #lnks=browser.find_elements(By.XPATH, "(//a[contains(@href,'/Reservations/Bookings')])")

    browser.get("https://app.courtreserve.com/Online/Reservations/Bookings/9705?sId=13790")

    next_day_button = browser.find_element(By.XPATH,"//button[@title='Next']")
    cur_date = browser.find_element(By.XPATH,"//span[@class='k-sm-date-format']").get_attribute("innerText")
    while date != cur_date:
        cur_date = browser.find_element(By.XPATH,"//span[@class='k-sm-date-format']").get_attribute("innerText")
        next_day_button.click()
    
    sleep(1)
    # find time slot
    #reserve = browser.find_elements(By.XPATH,'//button[(contains(@start, "18:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')
    #reserve = browser.find_elements(By.XPATH,'//button[(contains(@start, "19:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')
    reserve = browser.find_elements(By.XPATH,'//button[(contains(@start, "%s")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]'%str(TIMESLOT))

    if len(reserve)==0:
        print("No availiability")
        return

    if len(reserve) > 0:
        Court_Labels = ["Court 1", "Court 2", "Court 3", "Court 4"]
        #Priority_lane = [PRIORITY.index(0), PRIORITY.index(1), PRIORITY.index(2), PRIORITY.index(3)]
        priority_lane = []
        for available_slot in reserve:
            court_label = available_slot.get_attribute("courtlabel")
            priority_lane.append(PRIORITY[Court_Labels.index(court_label)])
        
        reserve_order = []
        for i in range(len(priority_lane)):
            # reserve order should be
            minimum = min(priority_lane)
            reserve_order.append(priority_lane.index(minimum))
            priority_lane.remove(minimum)

        booked = False
        i = 0
        while i < len(reserve) and not booked:
            # reserve court
            court_number = reserve_order[i]
            reserve[court_number].click()
            sleep(1)
            extra_player = browser.find_element(By.XPATH, '//input[@name="OwnersDropdown_input"]')
            extra_player.send_keys(SECOND_PLAYER)
            save_button = browser.find_element(By.XPATH, '//button[text()="Save"]')
            #save_button.click()
            booked = True
            print("Booked Timeslot at " + reserve[court_number].get_attribute("start") + " on "+ reserve[court_number].get_attribute("courtlabel"))
            i+=1


def format_date(target_date):
    Weekdays = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    weekday = Weekdays[target_date.weekday()]
    month = Months[int(target_date.strftime("%m")) - 1]
    date = target_date.strftime("%d")
    date_in_format = weekday + ", " + month + " " + date
    return date_in_format

def main():
    today = date.today()
    target_date = today + timedelta(days=7)
    target_date_in_format = format_date(target_date)
    browser = webdriver.Chrome()
    browser.get(COURT_RESERVE_PAGE)

    login(browser)
    sleep(0.5)
    #book_a_court(browser)
    book_a_court_at_certain_date(browser, target_date_in_format)

if __name__ == '__main__':
    main()