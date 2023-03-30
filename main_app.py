from selenium import webdriver
from selenium.webdriver.common.by import By



def login_petfriends(login:str,pswrd:str):
    # Open PetFriends base page:
    selenium = webdriver.Chrome()
    selenium.get("https://petfriends.skillfactory.ru/")

    # click on the new user button
    btn_newuser = selenium.find_element('xpath',str("//button[@onclick=\"document.location='/new_user';\"]"))
    btn_newuser.click()

    # click existing user button
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, u'У меня уже есть аккаунт')
    btn_exist_acc.click()

    # add email
    field_email = selenium.find_element('id',"email")
    field_email.clear()
    field_email.send_keys(login)

    # add password
    field_pass = selenium.find_element('id',"pass")
    field_pass.clear()
    field_pass.send_keys(pswrd)

    # click submit button
    btn_submit = selenium.find_element('xpath',"//button[@type='submit']")
    btn_submit.click()

    if selenium.current_url != 'https://petfriends.skillfactory.ru/all_pets':
        raise Exception("login error")
