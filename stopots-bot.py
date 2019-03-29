#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
import requests
import wget
import os
import time
import string
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cls():
  os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.headless = False
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
driver = webdriver.Firefox(options=options, executable_path='./geckodriver.exe', capabilities=firefox_capabilities)

letras = list(string.ascii_lowercase)
categorias = ["Adjetivo","Animal","App ou site","Ator","Banda","Cantor","Carro","Capital","Celebridade","CEP","Cidade",
              "Comida","Cor","Desenho animado","Eletro Eletrônico","Esporte","Esportista","Filme","Flor","FLV","Fruta",
              "Game","Gentílico","Inseto","Instrumento Musical","JLR","Líquido","Marca","Música","MSÉ","Nome Feminino",
              "Nome Masculino","Objeto","País","Palavra em inglês","PCH","PDA","Personagem Fictício","Profissão",
              "Programa de TV","Série","Sobremesa","Sobrenome","Time esportivo","Verbo","Vestuário"]

def update_dict():
  for letra in letras:
    url = "https://stopanswersapi.firebaseapp.com/api/answers/"+letra
    wget.download(url,"./dicionario/"+letra+".json")
  print("Dicionario Atualizado")

def joinGame(username):
  print("Joining...")
  wait = WebDriverWait(driver, 5)
  # entrar button
  wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="login"]/form/button')))
  driver.find_element_by_xpath('//*[@class="login"]/form/button').click()
  # username field
  wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="perfil"]//input')))
  driver.find_element_by_xpath('//*[@class="perfil"]//input').clear()
  driver.find_element_by_xpath('//*[@class="perfil"]//input').send_keys(username)
  time.sleep(3)
  driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]').click() # jogar button
  print("Joined as", username)

def find_letter():
  global letter
  try:
    letter = driver.find_element_by_xpath('//*[@id="letter"]/span').text
    print("Now Letter is:", letter)
    #return letter
  except: pass

def auto_complete(letter):
  #with open('./dicionario/'+letter) as current_letter:
  #  data = json.load(current_letter)

  #elements = driver.find_elements_by_class_name('ct answers')
  try:
    #items = driver.find_elements_by_xpath('//*[@class="ct answers"]//label')
    for x in range(1, 13):
      #item = driver.find_elements_by_xpath('//*[@class="ct answers"]//label['+str(x)+']')
      #item = driver.find_elements_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']')
      #item = driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']')
      item = driver.find_element(By.XPATH('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/..'))
      itemName = item.find_element(By.XPATH('./span/')).text

      print(itemName)

    #nomes = items.find_element_by_xpath('./span/').text
    #inputs = items.find_element_by_xpath('./input')
  except Exception as e: print(e)


  #'//*[@class="ct answers"]/div[2]/div[2]/div/div[1]/label[2]/span'

  #current_letter.close()

def playTheGame():
  while True:
    #cls()
    find_letter()
    time.sleep(5)
    auto_complete(letter)
    try:
      end = driver.find_element_by_class_name('ct end')
      if end: break
    except: pass


if __name__ == "__main__":
  print("Options:",
        "\n1 - Entrar no Jogo"
        "\n2 - Entrar com ID "
        "\n3 - Atualizar Dicionario"
        "\n4 - Sair")
  option = str(input("> "))
  #cls()

  if option == '1':
    username = input("Digite nome:")
    driver.get("https://stopots.com.br/")
    joinGame(username)
    time.sleep(10)
    playTheGame()

  if option == '2':
    id = str(input("ID:"))
    driver.get("https://stopots.com.br/"+id)
    time.sleep(5)
    playTheGame()

  if option == '3':
    update_dict()
