import requests
from bs4 import BeautifulSoup
from selenium import webdriver

old_string = ""
string = ""
s = requests.get("https://connection-robertoruano.c9users.io/PHP/log.html")
string = str(s.content)
while(1):
    if len(string)>len(old_string):
        character_numbers = len(old_string)-len(string)
        old_string= string
        commands=old_string[(character_numbers-1):-1]
        print(commands)
    s = requests.get("https://connection-robertoruano.c9users.io/PHP/log.html")
    string = str(s.content)
    #print(s.content)
    #browser = webdriver.Chrome("C:\chromedriver_win32\chromedriver")
    #browser.get("https://connection-robertoruano.c9users.io/key.html")


    #string = BeautifulSoup(s, 'html.parser')
    #commands = string.find(id='demo')



#browser.quit()