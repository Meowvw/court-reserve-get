from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep

USERNAME = "scw.lj330@gmail.com"
PASSWORD = "wbttzy52chen"
# priority for [6to7, 7to8, 8to9] sessions
PRIORITY = [2, 0, 1]
# priority for [court1, court2, court3, court4]
PRIORITY = [3, 2, 1, 0]

COURT_RESERVE_PAGE = "https://app.courtreserve.com/Online/Account/Login"

def login(browser):
    username_input = browser.find_element(By.CSS_SELECTOR,'input[id="UserNameOrEmail"]')
    pwd_input = browser.find_element(By.CSS_SELECTOR,'input[id="Password"]')

    username_input.send_keys(USERNAME)
    pwd_input.send_keys(PASSWORD)
    login = browser.find_element(By.CSS_SELECTOR,'button[type="button"]')
    login.click()

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
        reserve_8to9 = browser.find_elements(By.XPATH,'//button[(contains(@start, "20:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')
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
        #allentry = driver.find_elements(By.XPATH, "//div[contains(@class,'dw-cal-day')]")
#for date in allentry:
#
#    date_id = date.get_attribute('aria-label')
#    
#    #ignore those dates which are not selectable
#    if date.get_attribute('aria-disabled') == 'true' or date_id is None or date_id in list_entry:
#        pass
#    else:
#        list_entry += [date_id]                
#
#driver.refresh()
#        import pdb
#        pdb.set_trace()
#        reserve_8to9[0].click() 


    #browser.quit()
    #hover.perform()

    #element = browser.find_element(By.XPATH, "//a[contains(@href, '/Online/Reservation/Bookings')]")

def book_a_court_at_certain_date(browser, date):
    browser.maximize_window()
    #lnks=browser.find_elements(By.XPATH, "(//a[contains(@href,'/Reservations/Bookings')])")

    browser.get("https://app.courtreserve.com/Online/Reservations/Bookings/9705?sId=13790")

    next_day_button = browser.find_element(By.XPATH,"//button[@title='Next']")
    cur_date = browser.find_element(By.XPATH,"//span[@class='k-sm-date-format']").get_attribute("innerText")
    import pdb
    pdb.set_trace()
    while date != cur_date:
        cur_date = browser.find_element(By.XPATH,"//span[@class='k-sm-date-format']").get_attribute("innerText")
        next_day_button.click()
    
    sleep(1)
    # find time slot
    reserve_6to7 = browser.find_elements(By.XPATH,'//button[(contains(@start, "18:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')
    reserve_7to8 = browser.find_elements(By.XPATH,'//button[(contains(@start, "19:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')
    reserve_8to9 = browser.find_elements(By.XPATH,'//button[(contains(@start, "20:00:00 GMT-0400")) and (@class="btn btn-default btn-expanded-slot slot-btn m-auto")]')

    if len(reserve_6to7) == 0 and len(reserve_7to8)==0 and len(reserve_8to9)==0:
        print("No availiability")
        return

    if len(reserve_8to9) > 0:
        reserve_8to9.click()


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