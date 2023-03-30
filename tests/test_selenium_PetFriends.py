from main_app import login_petfriends
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

LOGIN='nesvitailo_alex@mail.ru'
PSWRD='!1234569870'
DRVR_DIR='D:/chromedriver_win32_109/chromedriver.exe'

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(DRVR_DIR)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_of_my_pets_table():
   # Вводим email
   pytest.driver.find_element(By.ID,'email').send_keys(LOGIN)
   # Вводим пароль
   pytest.driver.find_element(By.ID,'pass').send_keys(PSWRD)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()

   # Проверяем, что мы оказались на главной странице пользователя с ожиданием заголовка страницы
   WebDriverWait(pytest.driver, 10).until(EC.title_is('PetFriends: My Pets'))
   assert pytest.driver.find_element(By.TAG_NAME,'h1').text == "PetFriends"
   pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')

   # Получаем данные о пользователе c явным ожиданием элемента
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.\.col-sm-4.left')))
   my_data=pytest.driver.find_element(By.CSS_SELECTOR,'div.\.col-sm-4.left').text.split('\n')
   # Выделяем из полученных данных количество питомцев
   pet_sum=int(my_data[1].split(':')[1])

   # Получаем данные о питомцах с явным ожиданием элементов
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr')))
   pets = pytest.driver.find_elements(By.CSS_SELECTOR,'tbody tr')

   # Получаем данные о фото питомцев
   image_pet=pytest.driver.find_elements(By.CSS_SELECTOR,'tbody img')
   # Считаем количество питомцев с фото
   img_sum=0
   for i in range(len(pets)):
       image_pet[i]=image_pet[i].get_attribute('src')
       if image_pet[i]!='':
           img_sum+=1
   #Проверяем, чтобы хотябы половина питомцев была с фото
   assert img_sum>=((len(pets)//2)+(len(pets)%2))


   image_pet
   # Проверяем наличие на странице всех питомцев
   assert len(pets)==pet_sum
   name_pet=[]
   species_pet=[]
   age_pet=[]
   for i in range(len(pets)):
       #Выделяем атрибуты каждого из питомцев
       current_pet=pets[i].text.split(' ')
       name_pet.append(current_pet[0])
       species_pet.append(current_pet[1])
       age_pet.append(current_pet[2].split('\n')[0])
       #Проверяем наличие пустых параметров
       assert name_pet[i]!=''
       assert species_pet[i] != ''
       assert age_pet[i] != ''
   for i in range(len(pets)-1):
      for j in range(len(pets)-i-1):

         #Проверяем совпадение имён для всех уникальных пар питомцев
         assert name_pet[i]!=name_pet[j+i+1]
         #Проверяем совпадение питомцев для всех уникальных пар
         assert pets[i].text!=pets[j+i+1].text

def test_of_all_pets_card():

    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(LOGIN)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(PSWRD)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Добавляем неявное ожидание для загрузки всех элементов страницы
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('http://petfriends.skillfactory.ru/all_pets')


    images = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-img-top')

    names = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')

    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')

    for i in range(len(names)):

        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''

        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0



