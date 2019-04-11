#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import string
import re
import json
from selenium import webdriver
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
categorias = ["ADJETIVO","ANIMAL","APP OU SITE","ATOR","AVE","BANDA","BRINQUEDO",
              "CANTOR","CAPITAL","CARROCELEBRIDADE","CEP","CIDADE","COMIDA SAUDÁVEL",
              "COR","DESENHO ANIMADO","DOCE","DOENÇA","ELETRO ELETRÔNICO","ESPORTE",
              "ESPORTISTA","FANTASIA","FILME","FLOR","FLV","FRUTA","GAME","GENTÍLICO",
              "IDIOMA","INGREDIENTE","INSETO","INSTRUMENTO MUSICAL","JLR","LÍQUIDO",
              "MAMÍFERO","MARCA","MEIO DE TRANSPORTE","MSÉ","MÚSICA","NOME FEMININO",
              "NOME MASCULINO","OBJETO","PALAVRA EM ESPANHOL","PALAVRA EM INGLÊS","PAÍS",
              "PCH","PDA","PERSONAGEM FICTÍCIO","PRESENTE","PROFISSÃO","PROGRAMA DE TV",
              "RAÇA DE CACHORRO","REMÉDIO","SABOR DE PIZZA","SABOR DE SORVETE","SOBREMESA",
              "SOBRENOME","SUPER-HERÓI","SÉRIE","TIME ESPORTIVO","VERBO","VESTUÁRIO","VILÃO",
              "FLV"]

def joinGame(username):
  print("Entrando...")
  wait = WebDriverWait(driver, 10)
  # entrar button
  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="login"]/form/button')))
  driver.find_element_by_xpath('//*[@class="login"]/form/button').click()

  wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="load"]')))
  # username field
  if username != ' ':
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="perfil"]//input')))
    driver.find_element_by_xpath('//*[@class="perfil"]//input').clear()
    driver.find_element_by_xpath('//*[@class="perfil"]//input').send_keys(username)
  # jogar button
  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]')))
  time.sleep(1)
  driver.find_element_by_xpath('//*[@class="actions"]/button[@class="bt-yellow icon-exclamation"]/strong').click()
  print("Logado como:", username)

def find_letter():
  global letter
  try:
    letter = driver.find_element_by_xpath('//*[@id="letter"]/span').text
    print("Letra Atual:", letter)
  except: pass

def auto_complete(letter):
  print("Auto Completando...")
  with open('./dicionario/'+letter.lower()+'.json', 'r', encoding='utf-8') as current_letter:
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
          break
  except: pass
  current_letter.close()

def matchInfo():
  try:
    rounds = driver.find_element_by_xpath('//*[@class="rounds"]/span').text
    total = driver.find_element_by_xpath('//*[@class="rounds"]/p[2]').text
    print("- Rodadas:", rounds + total,"-")
  except: pass
  print("- Current Players -")
  for x in range(1, 15):
    try:
      nick = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/*[@class="nick"]').text
      pts = driver.find_element_by_xpath('//*[@id="users"]/li['+str(x)+']//*[@class="infos"]/span').text
      if nick:
        if nick == username: print(">",nick,"-",pts)
        else: print(nick,"-",pts)
    except: pass

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

def validate(type):
  if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
    if type == 'quick':
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
    elif type == 'deny':
      print("Negando todas as respostas...")
      for x in range(1, 15):
        if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/span').text == 'VALIDADO!':
          driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').click()
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
    elif type == 'check':
      print("Verificando Respostas...")
      with open('./dicionario/'+letter.lower()+'.json', 'r', encoding='utf-8') as current_letter:
        data = json.load(current_letter)
      try:
        categoria = driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]/div/h3').text
        strCategoria = re.sub('TEMA: ', '', categoria)
        for x in range(1, 15):
          if driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/span').text == 'VALIDADO!':
            categoryAnswer = driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').text
            if any(item['category'].lower() == strCategoria.lower() and item['answer'].lower() == categoryAnswer.lower() for item in data):
              continue
            else:
              driver.find_element_by_xpath('//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label['+str(x)+']/div').click()
              continue
      except: pass
      driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      current_letter.close()

def playTheGame():
  while True:
    cls()
    try:
      button = driver.find_element_by_xpath('//*[@class= "bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake" or @class="bt-yellow icon-exclamation disable"]/strong').text
      if button == 'STOP!':
        find_letter()
        auto_complete(letter)
      # Avaliador
      if button == 'AVALIAR':
        validate('check')
      # Rank fim de Round
      if driver.find_element_by_xpath('//*[@class="active"]//*[@class="trophy"]'):
        roundEndRank()
      # Estou pronto:
      if driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]'):
        driver.find_element_by_xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click()
      # AFK Detector:
      if driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button'):
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="alert"]//*[@class="buttons"]/button/strong').click()
      elif driver.find_elements_by_xpath('//*[@class="popup-enter-done"]'):
        pass
    except: pass
    matchInfo()
    time.sleep(3)

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
        "\n3 - Configs"
        "\n4 - Sair")
  option = str(input("> "))

  if option == '1':
    username = input("Digite nome: ")
    driver.get("https://stopots.com.br/")
    joinGame(username)
    playTheGame()

  if option == '2':
    id = str(input("ID:"))
    driver.get("https://stopots.com.br/"+id)
    time.sleep(5)
    playTheGame()

  if option == '3':
    pass

  if option == '4':
    exit()
