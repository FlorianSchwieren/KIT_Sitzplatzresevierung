from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


URL = "https://raumbuchung.bibliothek.kit.edu";
LOGIN_HREF = "/sitzplatzreservierung/admin.php";
BOOK_HREF = "/sitzplatzreservierung/edit_entry.php?area={area}&room={room}&period={period}&year={year}&month={month}&day={day}";
REPORT_HREF = "/sitzplatzreservierung/report.php?";

class Booking:

    def __init__(self, config):
        self.config = config;


    def book(self, period, year, month, day):
        driver = webdriver.Chrome();
        login(driver, self.config["username"], self.config["password"]);

        for seat in self.config["seat"]:
            driver.execute_script("window.open('{url}','{id}');".format(url = getSeatUrl(seat["area"], seat["id"], period, year, month, day), id = str(seat["id"])))

        time.sleep(0.5)
        for seat in self.config["seat"]:
            driver.switch_to.window(str(seat["id"]));
            policy_check_element = driver.find_element(By.ID, 'policy_check');
            while (policy_check_element.get_attribute("class") == "bad" and "Buchungstermin" in policy_check_element.get_attribute("title")):
                time.sleep(2)
                driver.refresh
                policy_check_element = driver.find_element(By.ID, 'policy_check');

            conflict_check_element = driver.find_element(By.ID, 'conflict_check');
            if (conflict_check_element.get_attribute("class") == "good"):
                driver.find_element(By.NAME, 'save_button').click();

                current_url = driver.current_url;
                if "edit_entry_handler.php" not in current_url:
                    driver.close();
                    return seat;
        driver.close();
        return None;

    def get_html_table(self):
        driver = webdriver.Chrome();
        login(driver, self.config["username"], self.config["password"]);

        driver.get(URL + REPORT_HREF)

        driver.find_element(By.CLASS_NAME, "submit").click();
        time.sleep(0.5)
        table_html = driver.find_element(By.CLASS_NAME, "dataTables_scroll").get_attribute('outerHTML');
        driver.close();
        return table_html;

    def get_config(self):
        return self.config;

        

def login(driver, username, password):
    driver.get(URL + LOGIN_HREF);
    user_name_element = driver.find_element(By.ID,  "NewUserName");
    user_name_element.send_keys(username);

    password_element = driver.find_element(By.ID, "NewUserPassword");
    password_element.send_keys(password);

    submit_element = driver.find_element(By.CLASS_NAME, "submit");
    submit_element.click();


    if '?' not in driver.current_url:
        raise Exception("Login not possible!")


def getSeatUrl(area, room, period, year, month, day):
    return URL + BOOK_HREF.format(area = area, room = room, period = period, year = year, month = month, day = day)
