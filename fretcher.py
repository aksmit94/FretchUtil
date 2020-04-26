from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import smtplib
import winsound


def zip_input(driver):
    zip_input = '/html/body/div[8]/div/div/div[2]/form/div[1]/input'
    zip_submit = '/html/body/div[8]/div/div/div[2]/form/div[3]/button[3]'
    driver.find_element_by_xpath(zip_input).send_keys('10017')
    driver.find_element_by_xpath(zip_submit).click()


def close_dialog(driver):
    dialog_close = '/html/body/div[2]/div/div[1]/a'
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, dialog_close)))
    driver.find_element_by_xpath(dialog_close).click()


def login(driver, username, password):
    login_menu = '/html/body/div[3]/header/div/div[3]/div[3]/div[3]/div/div/button'
    driver.find_element_by_xpath(login_menu).click()
    login_popup = '/html/body/div[3]/header/div/div[3]/div[3]/div[3]/div/div/div/ul/li[1]/a'
    driver.find_element_by_xpath(login_popup).click()

    username_input = '/html/body/div[7]/div[2]/section[1]/article/div[1]/form/div[3]/input'
    pass_input = '/html/body/div[7]/div[2]/section[1]/article/div[1]/form/div[4]/input'
    submit_input = '/html/body/div[7]/div[2]/section[1]/article/div[1]/form/div[5]/button'
    driver.find_element_by_xpath(username_input).send_keys(username)
    driver.find_element_by_xpath(pass_input).send_keys(password)
    driver.find_element_by_xpath(submit_input).click()


def dialog_close_after_login(driver):
    dialog_close = '/html/body/div[2]/div/div[1]/a'
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, dialog_close)))
    driver.find_element_by_xpath(dialog_close).click()


def get_delivery_slots(driver, trial):
    delivery_slot_dropdown = '/html/body/div[3]/header/div/div[3]/div[3]/div[2]/div/div/button'
    driver.find_element_by_xpath(delivery_slot_dropdown).click()
    delivery_window_div = driver.find_element_by_class_name('delivrBox')
    slots = delivery_window_div.find_elements_by_tag_name('li')
    times = []
    if len(slots) == 1:
        print(f'Trial no. {trial} -- No delivery slots available')
    else:
        for elem in slots:
            times.append(elem.text)
    return times


def send_email(receivers, slots=[]):
    gmail_user = ''
    gmail_password = ''

    sent_from = gmail_user
    to = receivers
    subject = 'Information about Fretch delivery windows'
    if slots:
        msg_string = ''
        for slot in slots:
            msg_string += '\n' + str(slot)
        body = "Following slots are found: " + msg_string
    else:
        body = "Nahi mila yaar slot :("

    email_text = f"""\
                From: {sent_from}
                To: {to}
                Subject: {subject} \n
        
                {body}
                """

    print(email_text)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')


if __name__ == '__main__':
    slots = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Using Chrome to access web
    # driver = webdriver.Chrome()

    # Open the website
    driver.get('https://mirchimarket.com')

    zip_input(driver)
    close_dialog(driver)

    username = ''
    password = ''
    login(driver, username, password)

    trial = 0
    
    # List of email addresses to inform
    receivers = []

    while not slots:
        trial += 1
        dialog_close_after_login(driver)
        slots = get_delivery_slots(driver, trial)
        print('Waiting before next request...')
        time.sleep(5)
        driver.refresh()

    if slots:
        for i in range(5):
            duration = 1000  # milliseconds
            freq = 800  # Hz
            winsound.Beep(freq, duration)

        print('Slots Found!!!')
        for receiver in receivers:
            send_email(receiver, slots=slots)
        print(slots)
