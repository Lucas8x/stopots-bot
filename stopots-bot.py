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
  wait = WebDriverWait(driver, 6)
  # entrar button
  wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="login"]/form/button')))
  driver.find_element_by_xpath('//*[@class="login"]/form/button').click()
  # username field
  if username != ' ':
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="perfil"]//input')))
    driver.find_element_by_xpath('//*[@class="perfil"]//input').clear()
    driver.find_element_by_xpath('//*[@class="perfil"]//input').send_keys(username)
  wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]')))
  driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]').click() # jogar button
  print("Joined as", username)

def find_letter():
  global letter
  try:
    letter = driver.find_element_by_xpath('//*[@id="letter"]/span').text
    print("Now Letter is:", letter)
  except: pass

def auto_complete(letter):
  with open('./dicionario/'+letter.lower()+'.json') as current_letter:
    data = json.load(current_letter)
  try:
    for x in range(1, 13):
      itemType = driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/span').text
      for item in data:
        if item['category'].lower() == itemType.lower():
          campo = driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/input').get_attribute('value')
          if campo == '':
            resposta = str(item['answer'])
            driver.find_element_by_xpath('//*[@class="ct answers" or @class="ct answers up-enter-done"]//label['+str(x)+']/input').send_keys(resposta)
          else: pass
          break
        else: pass
  except: pass
  current_letter.close()

def matchInfo():
  try:
    rounds = driver.find_element_by_xpath('//*[@class="rounds"]/span').text
    total = driver.find_element_by_xpath('//*[@class="rounds"]/p[2]').text
    print("Rodadas:", rounds + total)
  except: pass
  print("- Current Players -")
  for x in range(1, 15):
    try:
      nick = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/*[@class="nick"]').text
      pts = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/span').text
      if nick: print(nick,"-",pts)
    except:pass

def roundEndRank():
  print("- Rank End Round -")
  for x in range(1, 15):
    try:
      position = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="position"]/span').text
      nick = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="nick"]').text
      pts = driver.find_element_by_xpath('//*[@class="ct ranking" or @class="ct ranking up-enter-done"]//*[@class="scrollElements"]//li['+str(x)+']//*[@class="points"]').text
      if nick: print(position,"-",nick,"-",pts)
    except: pass
  print("\n")

def playTheGame():
  while True:
    cls()
    try:
      button = driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake" or @class="bt-yellow icon-exclamation disable"]/strong').text
      if button == 'STOP!':
        find_letter()
        time.sleep(1)
        auto_complete(letter)
      # Rank fim de Round
      if driver.find_element_by_xpath('//*[@class="active"]//*[@class="trophy"]'):
        roundEndRank()
      # Estou pronto:
      if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
        driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      # AFK Detector:
      if driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button'):
        driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button').click()
    except: pass
    matchInfo()
    time.sleep(5)

    '''
    try:
      end = driver.find_element_by_class_name('ct end')
      if end: break
    except: pass
    '''

if __name__ == "__main__":
  print("Options:",
        "\n1 - Entrar no Jogo"
        "\n2 - Entrar com ID "
        "\n3 - Atualizar Dicionario"
        "\n4 - Sair")
  option = str(input("> "))

  if option == '1':
    username = input("Digite nome:")
    driver.get("https://stopots.com.br/")
    joinGame(username)
    playTheGame()

  if option == '2':
    id = str(input("ID:"))
    driver.get("https://stopots.com.br/"+id)
    time.sleep(5)
    playTheGame()

  if option == '3':
    update_dict()

  if option == '4':
    exit()
